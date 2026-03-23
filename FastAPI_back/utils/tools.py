from typing import Dict, Any
from sqlalchemy import String, func, null, or_

def luhn_check(num: str) -> bool:
    total = 0
    reverse_digits = [int(d) for d in reversed(num)]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = digit * 2
            total += doubled if doubled < 10 else doubled - 9
        else:
            total += digit
    return total % 10 == 0







def get_column(schema_class, field: str):
    """
    Retrieve the column object from the schema class.
    Supports both direct fields and relationships.
    """
    if '__' in field:
        relationship, subfield = field.split('__', 1)
        related_class = getattr(schema_class, relationship).property.mapper.class_
        return getattr(related_class, subfield), relationship
    else:
        return getattr(schema_class, field), None

def join_relationship(query, schema_class, relationship, joined_relationships):
    if relationship and relationship not in joined_relationships:
        query = query.join(getattr(schema_class, relationship))
        joined_relationships.add(relationship)
    return query

def apply_filter(query, column, value, operator: str = 'ilike'):
    if operator == 'in':
        return query.filter(column.in_(value))
    elif operator == 'ilike':
        return query.filter(func.lower(column.cast(String)).ilike(f"%{str(value).lower()}%"))
    elif operator == 'isnull':
        return query.filter(column == None) if value else query.filter(column != None)
    else:
        raise ValueError(f"Unsupported filter operator: {operator}")

def handle_or_conditions(schema_class, query, fields, value, joined_relationships):
    or_conditions = []
    for field in fields:
        column, relationship = get_column(schema_class, field)
        query = join_relationship(query, schema_class, relationship, joined_relationships)
        or_conditions.append(func.lower(column.cast(String)).ilike(f"%{str(value).lower()}%"))
    return query.filter(or_(*or_conditions))



def build_filters(schema_class, query, filters: Dict[str, Any]) -> Any:
    joined_relationships = set()
    
    for attr, value in filters.items():
        try:
            if '_or_' in attr:
                fields = attr.split('_or_')
                query = handle_or_conditions(schema_class, query, fields, value, joined_relationships)
            elif attr.endswith('__in'):
                field_name = attr[:-4]  # Remove the '__in' suffix
                column, relationship = get_column(schema_class, field_name)
                query = join_relationship(query, schema_class, relationship, joined_relationships)
                query = apply_filter(query, column, value, operator='in')
            elif attr.endswith('__ilike'):
                field_name = attr[:-7]
                column, relationship = get_column(schema_class, field_name)
                query = join_relationship(query, schema_class, relationship, joined_relationships)
                query = apply_filter(query, column, value, operator='ilike')
            elif attr.endswith('__isnull'):
                field_name = attr[:-8]  # Remove the '__isnull' suffix
                column, relationship = get_column(schema_class, field_name)
                query = join_relationship(query, schema_class, relationship, joined_relationships)
                query = apply_filter(query, column, value, operator='isnull')
            else:
                column, relationship = get_column(schema_class, attr)
                query = join_relationship(query, schema_class, relationship, joined_relationships)
                query = apply_filter(query, column, value)
        except AttributeError:
            print(f"Attribute '{attr}' not found in the schema '{schema_class.__name__}'")
            continue
    
    return query