import { useEffect, useMemo, useRef, useState } from 'react'
import { Group, Image as KonvaImage, Layer, Rect, Stage, Text, Transformer } from 'react-konva'
import './App.css'
import heroImage from './assets/img3-Photoroom.png'
import artistImage from './assets/section2.png'
import catalogImage from './assets/Property 1=Variant4.png'
import lookbookImage from './assets/Property 1=Variant5.png'
import logo from './assets/Logo 2.png'
import heroTitle from './assets/costumize your own design.png'
import img2  from './assets/img2.png'

function HomePage({ onStartDesigning }) {
  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <img className="hero-title" src={heroTitle} alt="Customize your own design" />
        </div>
      </section>

      <section className="highlight">
        <div className="highlight-card">
          <span>Personalized, versatile, self-pleasing</span>
        </div>
      </section>

      <section className="artists">
        <div className="artists-image">
          <img src={artistImage} alt="Artist phone case" />
        </div>
        <div className="artists-content">
          <h2>Your Way Artists</h2>
          <p>
            Bring your imagination to life.
Turn your phone into a canvas with vibrant collaborations and expressive designs — all on a blazing-fast website with zero sign-up or authentication required.
          </p>
          <div className="artists-actions">
            <button type="button" className="btn-primary" onClick={onStartDesigning}>
              Start Designing
            </button>
          </div>
        </div>
      </section>

      <section className="catalog">
        <div className="catalog-content">
          <h2>Create your own personal masterpiece.</h2>
          <p>
            Upload your photos, customize every detail, and turn your memories into a unique phone case that you can carry in your pocket.
          </p>
          <button type="button" className="btn-primary" onClick={onStartDesigning}>
            Start Designing
          </button>
        </div>
        <div className="catalog-image">
          <img src={catalogImage} alt="Phone case collection" />
        </div>
      </section>

      <section className="lookbook">
        <h2>#YourWayLookBook</h2>
        <div className="lookbook-grid">
          {[heroImage, img2, catalogImage, lookbookImage].map((image, index) => (
            <div className="lookbook-card" key={index}>
              <img src={image} alt={`Lookbook ${index + 1}`} />
            </div>
          ))}
        </div>
      </section>
    </>
  )
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

function CustomizeLandingPage({ onSelectFromScratch }) {
  return (
    <section className="customize-page">
      <div className="customize-layout">
        <div className="customize-main">
          <div className="customize-card">
            <h1>Click to Start</h1>
            <div className="customize-option-grid">
              <button type="button" className="customize-option-card" onClick={onSelectFromScratch}>
                <h3>Design from scratch</h3>
                <p>Select a blank case, then add your own design.</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function CaseCatalogPage({ title, subtitle, actionLabel, onBack, onSelectCase, includeTemplates = false }) {
  const [phoneCases, setPhoneCases] = useState([])
  const [templates, setTemplates] = useState([])
  const [phoneModels, setPhoneModels] = useState([])
  const [caseTypes, setCaseTypes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [selectedModelId, setSelectedModelId] = useState('')
  const [selectedCaseTypeId, setSelectedCaseTypeId] = useState('')

  useEffect(() => {
    let isMounted = true
    const fetchData = async () => {
      try {
        setIsLoading(true)
        const requests = [
          fetch(`${API_BASE}/phones/phone-cases`),
          fetch(`${API_BASE}/phones/phone-models`),
          fetch(`${API_BASE}/phones/case-types`),
        ]
        if (includeTemplates) {
          requests.push(fetch(`${API_BASE}/phones/phone-case-templates`))
        }
        const responses = await Promise.all(requests)
        const [casesJson, modelsJson, caseTypesJson, templatesJson] = await Promise.all(
          responses.map((response) => response.json()),
        )

        if (!isMounted) return
        setPhoneCases(casesJson?.result ?? [])
        setPhoneModels(modelsJson?.result ?? [])
        setCaseTypes(caseTypesJson?.result ?? [])
        setTemplates(includeTemplates ? templatesJson?.result ?? [] : [])
        setLoadError('')
      } catch (error) {
        if (!isMounted) return
        setLoadError('Failed to load cases. Please try again later.')
      } finally {
        if (!isMounted) return
        setIsLoading(false)
      }
    }

    fetchData()
    return () => {
      isMounted = false
    }
  }, [includeTemplates])

  const phoneModelById = useMemo(() => {
    const map = new Map()
    phoneModels.forEach((model) => map.set(model.id, model))
    return map
  }, [phoneModels])

  const caseTypeById = useMemo(() => {
    const map = new Map()
    caseTypes.forEach((caseType) => map.set(caseType.id, caseType))
    return map
  }, [caseTypes])

  const modelsForBrand = useMemo(() => {
    const extractNumber = (name) => {
      if (!name) return Number.POSITIVE_INFINITY
      const match = String(name).match(/\d+(?:\.\d+)?/)
      return match ? Number(match[0]) : Number.POSITIVE_INFINITY
    }
    return [...phoneModels].sort((a, b) => {
      const aNum = extractNumber(a.model_name)
      const bNum = extractNumber(b.model_name)
      if (aNum !== bNum) return aNum - bNum
      return String(a.model_name).localeCompare(String(b.model_name))
    })
  }, [phoneModels])

  const filteredCases = useMemo(() => {
    return phoneCases.filter((item) => {
      if (item?.active === false) return false
      if (selectedModelId && Number(selectedModelId) !== item.phone_model_id) return false
      if (selectedCaseTypeId && Number(selectedCaseTypeId) !== item.case_type_id) return false
      return true
    })
  }, [phoneCases, selectedModelId, selectedCaseTypeId])

  return (
    <section className="customize-page">
      <div className="customize-layout">
        <div className="customize-main">
          <div className="customize-card">
            <div className="case-catalog-header">
              <div>
                <h1>{title}</h1>
                {subtitle ? <p className="case-catalog-subtitle">{subtitle}</p> : null}
              </div>
              <button type="button" className="case-back" onClick={onBack}>
                ← Back
              </button>
            </div>

            <div className="case-filters">
              <label className="filter-group">
                <span className="filter-label">Model</span>
                <select
                  className="filter-select"
                  value={selectedModelId}
                  onChange={(event) => setSelectedModelId(event.target.value)}
                >
                  <option value="">All models</option>
                  {modelsForBrand.map((model) => (
                    <option key={model.id} value={model.id}>
                      {model.model_name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="filter-group">
                <span className="filter-label">Case type</span>
                <select
                  className="filter-select"
                  value={selectedCaseTypeId}
                  onChange={(event) => setSelectedCaseTypeId(event.target.value)}
                >
                  <option value="">All types</option>
                  {caseTypes.map((caseType) => (
                    <option key={caseType.id} value={caseType.id}>
                      {caseType.type_name}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            {isLoading ? (
              <p className="case-loading">Loading cases...</p>
            ) : loadError ? (
              <p className="case-loading">{loadError}</p>
            ) : (
              <div className="case-grid">
                {filteredCases.length === 0 ? (
                  <p className="case-loading">No cases available for these filters.</p>
                ) : (
                  filteredCases.map((item) => {
                    const model = phoneModelById.get(item.phone_model_id)
                    const caseType = caseTypeById.get(item.case_type_id)
                    return (
                      <div className="case-option" key={item.id}>
                        <div className="case-image">
                          <img
                            src={item.thumbnail_url || heroImage}
                            alt={item.title || 'Phone case'}
                          />
                        </div>
                        <div className="case-meta">
                          <h4>{item.title || `${model?.brand ?? ''} ${model?.model_name ?? ''}`}</h4>
                          {item?.price != null ? (
                            <p className="case-price">AED {Number(item.price).toFixed(2)}</p>
                          ) : null}
                          <div className="case-tags">
                            {model?.brand ? <span className="case-tag">{model.brand}</span> : null}
                            {model?.model_name ? (
                              <span className="case-tag">{model.model_name}</span>
                            ) : null}
                            {caseType?.type_name ? (
                              <span className="case-tag">{caseType.type_name}</span>
                            ) : null}
                          </div>
                        </div>
                        {onSelectCase ? (
                          <div className="case-actions">
                            <button
                              className="case-select"
                              onClick={() =>
                                onSelectCase?.(
                                  item,
                                  templates.find((template) => template.phone_case_id === item.id) ??
                                    null,
                                  phoneModelById.get(item.phone_model_id) ?? null,
                                  caseTypeById.get(item.case_type_id) ?? null,
                                )
                              }
                            >
                              {actionLabel}
                            </button>
                          </div>
                        ) : null}
                      </div>
                    )
                  })
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

function CustomizationPage({ onBack, phoneCase, template, phoneModel, caseType }) {
  const initialTexts = useMemo(
    () => [],
    [],
  )
  const [texts, setTexts] = useState(initialTexts)
  const [selectedId, setSelectedId] = useState(initialTexts[0]?.id)
  const [selectedDesignId, setSelectedDesignId] = useState(null)
  const [designElements, setDesignElements] = useState([])
  const [history, setHistory] = useState([{ texts: initialTexts, designs: [] }])
  const [baseImage, setBaseImage] = useState(null)
  const [overlayImage, setOverlayImage] = useState(null)
  const [maskImage, setMaskImage] = useState(null)
  const [caseBounds, setCaseBounds] = useState(null)
  const [cameraBounds, setCameraBounds] = useState(null)
  const [overlayDraw, setOverlayDraw] = useState(null)
  const [isTextLibraryOpen, setIsTextLibraryOpen] = useState(false)
  const [isColorPaletteOpen, setIsColorPaletteOpen] = useState(false)
  const [isDesignsOpen, setIsDesignsOpen] = useState(false)
  const [isArtworkOpen, setIsArtworkOpen] = useState(false)
  const [zoom, setZoom] = useState(1)
  const [activeTab, setActiveTab] = useState('edit')
  const [previewDataUrl, setPreviewDataUrl] = useState('')
  const [isExporting, setIsExporting] = useState(false)
  const [exportMode, setExportMode] = useState('none')
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false)
  const [isCheckoutSubmitting, setIsCheckoutSubmitting] = useState(false)
  const [checkoutError, setCheckoutError] = useState('')
  const [checkoutSuccess, setCheckoutSuccess] = useState(null)
  const [checkoutForm, setCheckoutForm] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    postal: '',
    magsafe: false,
  })
  const [editingTextId, setEditingTextId] = useState(null)
  const [editingValue, setEditingValue] = useState('')
  const [editingBox, setEditingBox] = useState(null)
  const [stageDimensions, setStageDimensions] = useState({ width: 420, height: 600 })
  const transformerRef = useRef(null)
  const stageRef = useRef(null)
  const editorCanvasRef = useRef(null)
  const textNodeRefs = useRef({})
  const designNodeRefs = useRef({})
  const uploadInputRef = useRef(null)
  const textEditorRef = useRef(null)
    const handleWheelZoom = (event) => { 
      event.evt.preventDefault()
      const scaleBy = 1.02
      const stage = stageRef.current
      if (!stage) return
      const oldScale = zoom
      const pointer = stage.getPointerPosition()
      if (!pointer) return

      const mousePointTo = {
        x: (pointer.x - stage.x()) / oldScale,
        y: (pointer.y - stage.y()) / oldScale,
      }

      const direction = event.evt.deltaY > 0 ? -1 : 1
      const nextScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy
      const clampedScale = Math.max(0.5, Math.min(2, Number(nextScale.toFixed(3))))

      setZoom(clampedScale)

      const newPos = {
        x: pointer.x - mousePointTo.x * clampedScale,
        y: pointer.y - mousePointTo.y * clampedScale,
      }
      stage.position(newPos)
      stage.batchDraw()
    }
  const handleWheelZoomOnContainer = (event) => {
    const stage = stageRef.current
    if (!stage) return
    stage.setPointersPositions(event)
    const pointer = stage.getPointerPosition()
    if (!pointer) return
    if (!caseBounds) return
    const isInsideCase =
      pointer.x >= caseBounds.x &&
      pointer.x <= caseBounds.x + caseBounds.width &&
      pointer.y >= caseBounds.y &&
      pointer.y <= caseBounds.y + caseBounds.height
    if (!isInsideCase) return
    event.preventDefault()
    handleWheelZoom({ evt: event })
  }

  useEffect(() => {
    const container = editorCanvasRef.current
    if (!container) return undefined
    const onWheel = (event) => handleWheelZoomOnContainer(event)
    container.addEventListener('wheel', onWheel, { passive: false })
    return () => container.removeEventListener('wheel', onWheel)
  }, [handleWheelZoomOnContainer])
  useEffect(() => {
    const updateDimensions = () => {
      const container = editorCanvasRef.current
      if (container) {
        // Adjust padding as needed
        const maxW = Math.min(container.clientWidth || 420, 420)
        setStageDimensions({ width: maxW, height: 600 })
      }
    }
    updateDimensions()
    window.addEventListener('resize', updateDimensions)
    return () => window.removeEventListener('resize', updateDimensions)
  }, [])

  const maxStageWidth = stageDimensions.width
  const maxStageHeight = stageDimensions.height
  const stageScale = template?.width_px && template?.height_px
    ? Math.min(maxStageWidth / template.width_px, maxStageHeight / template.height_px)
    : 1
  const stageWidth = template?.width_px
    ? Math.round(template.width_px * stageScale)
    : 420
  const stageHeight = template?.height_px
    ? Math.round(template.height_px * stageScale)
    : 620
  const dotPatternImage = useMemo(() => {
    if (typeof document === 'undefined') return null
    const patternCanvas = document.createElement('canvas')
    patternCanvas.width = 12
    patternCanvas.height = 12
    const ctx = patternCanvas.getContext('2d')
    if (!ctx) return null
    ctx.fillStyle = 'rgba(120, 120, 120, 0.35)'
    ctx.beginPath()
    ctx.arc(2.5, 2.5, 1.6, 0, Math.PI * 2)
    ctx.fill()
    return patternCanvas
  }, [])
  const safeInset = caseBounds
    ? Math.round(Math.min(caseBounds.width, caseBounds.height) * 0.06)
    : 0
  const hasTemplateAssets = Boolean(
    template?.base_image_url || template?.print_mask_url || template?.overlay_image_url,
  )
  const isTemplateReady = Boolean(caseBounds && (maskImage || baseImage))
  const isPreviewMode = activeTab === 'preview' || isExporting
  const isPrintExport = exportMode === 'print'
  const stageBackground = isPrintExport ? '#ffffff' : 'transparent'
  const showBaseImage = false
  const minTextFontSize = 8
  const defaultTextBoxWidth = 220
  const printPixelRatio =
    template?.width_px && stageWidth ? Math.max(1, template.width_px / stageWidth) : 4
  const colorOptions = [
    '#5b3a00',
    '#ff7a00',
    '#ffb500',
    '#2f2f2f',
    '#ffffff',
    '#6f2dbd',
    '#0f4c81',
    '#00a896',
    '#f94144',
    '#ff6fb1',
    '#3a86ff',
    '#2a9d8f',
    '#e76f51',
    '#264653',
  ]
  const textStyleGroups = useMemo(
    () => [
      {
        id: 'designed',
        title: 'Designed',
        items: [
          {
            id: 'style-1',
            label: 'Dreamy',
            text: 'Dreamy',
            fontFamily: 'Pacifico',
            fontSize: 28,
            color: '#ff7a00',
          },
          {
            id: 'style-2',
            label: 'Classic',
            text: 'Classic',
            fontFamily: 'Playfair Display',
            fontSize: 26,
            color: '#5b3a00',
          },
          {
            id: 'style-3',
            label: 'Modern',
            text: 'Modern',
            fontFamily: 'Montserrat',
            fontSize: 24,
            color: '#2f2f2f',
          },
          {
            id: 'style-4',
            label: 'Bold',
            text: 'Bold',
            fontFamily: 'Rubik Mono One',
            fontSize: 24,
            color: '#ffb500',
          },
          {
            id: 'style-5',
            label: 'Signature',
            text: 'Signature',
            fontFamily: 'Great Vibes',
            fontSize: 30,
            color: '#7a4a00',
          },
          {
            id: 'style-6',
            label: 'Retro',
            text: 'Retro',
            fontFamily: 'Bebas Neue',
            fontSize: 28,
            color: '#ff7a00',
          },
        ],
      },
      {
        id: 'favorites',
        title: 'Popular',
        items: [
          {
            id: 'style-7',
            label: 'Forever',
            text: 'Forever',
            fontFamily: 'Lobster',
            fontSize: 28,
            color: '#5b3a00',
          },
          {
            id: 'style-8',
            label: 'Vibe',
            text: 'Vibe',
            fontFamily: 'Oswald',
            fontSize: 26,
            color: '#2f2f2f',
          },
        ],
      },
    ],
    [],
  )
  const textDesignItems = useMemo(() => {
    const modules = import.meta.glob('./assets/text designs/*.{png,jpg,jpeg,svg}', {
      eager: true,
      import: 'default',
    })
    return Object.entries(modules).map(([path, src]) => {
      const name = path.split('/').pop()?.split('.').slice(0, -1).join('.') ?? 'Design'
      return { id: path, src, name }
    })
  }, [])

  const artworkDesignItems = useMemo(() => {
    const modules = import.meta.glob('./assets/designs/*.{png,jpg,jpeg,svg}', {
      eager: true,
      import: 'default',
    })
    return Object.entries(modules).map(([path, src]) => {
      const name = path.split('/').pop()?.split('.').slice(0, -1).join('.') ?? 'Design'
      return { id: path, src, name }
    })
  }, [])
  const fontOptions = useMemo(
    () => [
      { label: 'Itim', value: 'Itim' },
      { label: 'Montserrat', value: 'Montserrat' },
      { label: 'Sora', value: 'Sora' },
      { label: 'Playfair', value: 'Playfair Display' },
      { label: 'Cinzel', value: 'Cinzel' },
      { label: 'Abril Fatface', value: 'Abril Fatface' },
      { label: 'Pacifico', value: 'Pacifico' },
      { label: 'Dancing Script', value: 'Dancing Script' },
      { label: 'Caveat', value: 'Caveat' },
      { label: 'Great Vibes', value: 'Great Vibes' },
      { label: 'Bebas Neue', value: 'Bebas Neue' },
      { label: 'Teko', value: 'Teko' },
      { label: 'Oswald', value: 'Oswald' },
      { label: 'Righteous', value: 'Righteous' },
      { label: 'Lobster', value: 'Lobster' },
      { label: 'Rubik Mono', value: 'Rubik Mono One' },
    ],
    [],
  )

  const selectedText = texts.find((item) => item.id === selectedId)
  const selectedDesign = designElements.find((item) => item.id === selectedDesignId)
  const isSelectedTextBold = (selectedText?.fontStyle ?? '').includes('bold')
  const isSelectedTextItalic = (selectedText?.fontStyle ?? '').includes('italic')
  const selectedElementOpacity = selectedText?.opacity ?? selectedDesign?.opacity ?? 1

  const resolveFontStyle = (isBold, isItalic) => {
    if (isBold && isItalic) return 'bold italic'
    if (isBold) return 'bold'
    if (isItalic) return 'italic'
    return 'normal'
  }

  const handleTogglePanel = (panel) => {
    if (panel === 'library') {
      setIsTextLibraryOpen((value) => {
        const next = !value
        if (next) {
          setIsColorPaletteOpen(false)
          setIsDesignsOpen(false)
          setIsArtworkOpen(false)
        }
        return next
      })
      return
    }
    if (panel === 'color') {
      setIsColorPaletteOpen((value) => {
        const next = !value
        if (next) {
          setIsTextLibraryOpen(false)
          setIsDesignsOpen(false)
          setIsArtworkOpen(false)
        }
        return next
      })
      return
    }
    if (panel === 'designs') {
      setIsDesignsOpen((value) => {
        const next = !value
        if (next) {
          setIsTextLibraryOpen(false)
          setIsColorPaletteOpen(false)
          setIsArtworkOpen(false)
        }
        return next
      })
      return
    }
    if (panel === 'artwork') {
      setIsArtworkOpen((value) => {
        const next = !value
        if (next) {
          setIsTextLibraryOpen(false)
          setIsColorPaletteOpen(false)
          setIsDesignsOpen(false)
        }
        return next
      })
    }
  }

  const commitScene = (
    nextTexts,
    nextDesigns,
    nextSelectedTextId = selectedId,
    nextSelectedDesignId = selectedDesignId,
  ) => {
    setTexts(nextTexts)
    setDesignElements(nextDesigns)
    setSelectedId(nextSelectedTextId ?? null)
    setSelectedDesignId(nextSelectedDesignId ?? null)
    setHistory((prev) => [...prev, { texts: nextTexts, designs: nextDesigns }])
  }

  const commitTexts = (nextTexts, nextSelectedId = selectedId) => {
    const resolvedSelectedId = nextSelectedId ?? nextTexts[0]?.id ?? null
    commitScene(nextTexts, designElements, resolvedSelectedId, null)
  }

  const commitDesigns = (nextDesigns, nextSelectedDesignId = selectedDesignId) => {
    const resolvedSelectedDesignId = nextSelectedDesignId ?? nextDesigns[0]?.id ?? null
    commitScene(texts, nextDesigns, null, resolvedSelectedDesignId)
  }

  const handleDragEnd = (id, event) => {
    const nextPosition = event.target.position()
    const nextTexts = texts.map((item) =>
      item.id === id ? { ...item, ...nextPosition } : item,
    )
    commitTexts(nextTexts)
  }

  const handleAddText = (style) => {
    if (!caseBounds) return
    const maxZIndex = Math.max(
      0,
      ...texts.map((item) => item.zIndex ?? 0),
      ...designElements.map((item) => item.zIndex ?? 0),
    )
    const id = `t${Date.now()}`
    const x = caseBounds.x + caseBounds.width / 2 - defaultTextBoxWidth / 2
    const y = caseBounds.y + caseBounds.height / 2 - 12
    const resolvedStyle = typeof style === 'string' ? { text: style } : style
    const newText = {
      id,
      text: resolvedStyle?.text ?? 'Your Way',
      x,
      y,
      color: resolvedStyle?.color ?? '#5b3a00',
      fontSize: resolvedStyle?.fontSize ?? 22,
      fontFamily: resolvedStyle?.fontFamily ?? 'Itim',
      fontStyle: resolvedStyle?.fontStyle ?? 'normal',
      letterSpacing: resolvedStyle?.letterSpacing ?? 0,
      opacity: resolvedStyle?.opacity ?? 1,
      width: resolvedStyle?.width ?? defaultTextBoxWidth,
      zIndex: maxZIndex + 10,
    }
    commitTexts([...texts, newText], id)
    setSelectedDesignId(null)
  }

  const handleAddDesign = (src) => {
    if (!caseBounds) return
    const maxZIndex = Math.max(
      0,
      ...texts.map((item) => item.zIndex ?? 0),
      ...designElements.map((item) => item.zIndex ?? 0),
    )
    const id = `d${Date.now()}`
    const baseSize = 160
    const x = caseBounds.x + caseBounds.width / 2 - baseSize / 2
    const y = caseBounds.y + caseBounds.height / 2 - baseSize / 2
    const image = new window.Image()
    image.crossOrigin = 'anonymous'
    image.src = src
    const newDesign = {
      id,
      src,
      image,
      x,
      y,
      width: baseSize,
      height: baseSize,
      rotation: 0,
      opacity: 1,
      zIndex: maxZIndex + 10,
    }
    commitDesigns([...designElements, newDesign], id)

    image.onload = () => {
      const ratio = image.width && image.height ? image.height / image.width : 1
      setDesignElements((prev) =>
        prev.map((item) =>
          item.id === id ? { ...item, width: baseSize, height: baseSize * ratio } : item,
        ),
      )
    }
  }

  const handleUploadDesigns = (event) => {
    const files = Array.from(event.target.files || [])
    if (files.length === 0) return
    files.forEach((file) => {
      const objectUrl = URL.createObjectURL(file)
      handleAddDesign(objectUrl)
    })
    event.target.value = ''
  }

  const handleTextChange = (value) => {
    if (!selectedId) return
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, text: value } : item,
    )
    commitTexts(nextTexts)
  }

  const handleInlineChange = (value) => {
    setEditingValue(value)
    if (!editingTextId) return
    const nextTexts = texts.map((item) =>
      item.id === editingTextId ? { ...item, text: value } : item,
    )
    setTexts(nextTexts)
  }

  const startInlineTextEdit = (id) => {
    const current = texts.find((item) => item.id === id)
    if (!current) return
    const node = textNodeRefs.current[id]
    const stage = stageRef.current
    const container = editorCanvasRef.current
    if (!node || !stage || !container) return

    const stageRect = stage.container().getBoundingClientRect()
    const canvasRect = container.getBoundingClientRect()
    const scale = stage.scaleX() || 1
    const rect = node.getClientRect({ relativeTo: stage })

    setEditingTextId(id)
    setEditingValue(current.text)
    setEditingBox({
      left: stageRect.left - canvasRect.left + rect.x * scale + stage.x(),
      top: stageRect.top - canvasRect.top + rect.y * scale + stage.y(),
      width: Math.max(80, rect.width * scale),
      height: Math.max(28, rect.height * scale),
    })

    setTimeout(() => {
      textEditorRef.current?.focus()
      textEditorRef.current?.select()
    }, 0)
  }

  const finishInlineTextEdit = (commit) => {
    if (!editingTextId) return
    if (commit) {
      const nextTexts = texts.map((item) =>
        item.id === editingTextId ? { ...item, text: editingValue } : item,
      )
      commitTexts(nextTexts, editingTextId)
    }
    setEditingTextId(null)
    setEditingValue('')
    setEditingBox(null)
  }

  const handleInlineKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      finishInlineTextEdit(true)
    }
    if (event.key === 'Escape') {
      event.preventDefault()
      finishInlineTextEdit(false)
    }
  }

  const handleFontFamilyChange = (value) => {
    if (!selectedId) return
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, fontFamily: value } : item,
    )
    commitTexts(nextTexts)
  }

  const handleFontSizeInput = (value) => {
    if (!selectedId) return
    const numeric = Number(value)
    if (!Number.isFinite(numeric)) return
    const nextSize = Math.min(96, Math.max(minTextFontSize, numeric))
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, fontSize: nextSize } : item,
    )
    commitTexts(nextTexts)
  }

  const handleToggleBold = () => {
    if (!selectedId) return
    const nextTexts = texts.map((item) => {
      if (item.id !== selectedId) return item
      const fontStyle = item.fontStyle ?? 'normal'
      const hasBold = fontStyle.includes('bold')
      const hasItalic = fontStyle.includes('italic')
      const nextStyle = resolveFontStyle(!hasBold, hasItalic)
      return { ...item, fontStyle: nextStyle }
    })
    commitTexts(nextTexts)
  }

  const handleToggleItalic = () => {
    if (!selectedId) return
    const nextTexts = texts.map((item) => {
      if (item.id !== selectedId) return item
      const fontStyle = item.fontStyle ?? 'normal'
      const hasBold = fontStyle.includes('bold')
      const hasItalic = fontStyle.includes('italic')
      const nextStyle = resolveFontStyle(hasBold, !hasItalic)
      return { ...item, fontStyle: nextStyle }
    })
    commitTexts(nextTexts)
  }

  const handleAlignChange = (align) => {
    if (!selectedId) return
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, align } : item,
    )
    commitTexts(nextTexts)
  }

  const handleColorChange = (color) => {
    if (!selectedId) return
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, color } : item,
    )
    commitTexts(nextTexts)
  }

  const handleFontSizeChange = (delta) => {
    if (!selectedId) return
    const nextTexts = texts.map((item) => {
      if (item.id !== selectedId) return item
      const nextSize = Math.min(64, Math.max(minTextFontSize, (item.fontSize ?? 22) + delta))
      return { ...item, fontSize: nextSize }
    })
    commitTexts(nextTexts)
  }

  const handleLetterSpacingChange = (value) => {
    if (!selectedId) return
    const numeric = Number(value)
    if (!Number.isFinite(numeric)) return
    const nextSpacing = Math.max(0, Math.min(12, numeric))
    const nextTexts = texts.map((item) =>
      item.id === selectedId ? { ...item, letterSpacing: nextSpacing } : item,
    )
    commitTexts(nextTexts)
  }

  const handleElementOpacityChange = (value) => {
    const numeric = Number(value)
    if (!Number.isFinite(numeric)) return
    const nextOpacity = Math.max(0.15, Math.min(1, numeric))
    if (selectedId) {
      const nextTexts = texts.map((item) =>
        item.id === selectedId ? { ...item, opacity: nextOpacity } : item,
      )
      commitTexts(nextTexts)
      return
    }
    if (selectedDesignId) {
      const nextDesigns = designElements.map((item) =>
        item.id === selectedDesignId ? { ...item, opacity: nextOpacity } : item,
      )
      commitDesigns(nextDesigns, selectedDesignId)
    }
  }

  const duplicateSelected = () => {
    const maxZIndex = Math.max(
      0,
      ...texts.map((item) => item.zIndex ?? 0),
      ...designElements.map((item) => item.zIndex ?? 0),
    )
    if (selectedId) {
      const source = texts.find((item) => item.id === selectedId)
      if (!source) return
      const duplicate = {
        ...source,
        id: `t${Date.now()}`,
        x: source.x + 14,
        y: source.y + 14,
        zIndex: maxZIndex + 10,
      }
      commitTexts([...texts, duplicate], duplicate.id)
      return
    }
    if (selectedDesignId) {
      const source = designElements.find((item) => item.id === selectedDesignId)
      if (!source) return
      const duplicate = {
        ...source,
        id: `d${Date.now()}`,
        x: source.x + 14,
        y: source.y + 14,
        zIndex: maxZIndex + 10,
      }
      commitDesigns([...designElements, duplicate], duplicate.id)
    }
  }

  const nudgeSelected = (dx, dy) => {
    if (selectedId) {
      const nextTexts = texts.map((item) =>
        item.id === selectedId ? { ...item, x: item.x + dx, y: item.y + dy } : item,
      )
      commitTexts(nextTexts, selectedId)
      return
    }
    if (selectedDesignId) {
      const nextDesigns = designElements.map((item) =>
        item.id === selectedDesignId
          ? { ...item, x: item.x + dx, y: item.y + dy }
          : item,
      )
      commitDesigns(nextDesigns, selectedDesignId)
    }
  }

  const commitTransform = (id, node) => {
    if (!node) return
    const scaleX = node.scaleX() || 1
    const scaleY = node.scaleY() || 1
    const nextSize = Math.min(
      96,
      Math.max(minTextFontSize, (node.fontSize() ?? 22) * Math.max(scaleX, scaleY)),
    )
    const nextTexts = texts.map((item) =>
      item.id === id
        ? { ...item, x: node.x(), y: node.y(), fontSize: nextSize, rotation: node.rotation() }
        : item,
    )
    node.fontSize(nextSize)
    node.scaleX(1)
    node.scaleY(1)
    commitTexts(nextTexts, id)
  }

  const commitDesignTransform = (id, node) => {
    if (!node) return
    const scaleX = node.scaleX() || 1
    const scaleY = node.scaleY() || 1
    const nextWidth = Math.max(30, node.width() * scaleX)
    const nextHeight = Math.max(30, node.height() * scaleY)
    node.scaleX(1)
    node.scaleY(1)
    const nextDesigns = designElements.map((design) =>
      design.id === id
        ? {
            ...design,
            x: node.x(),
            y: node.y(),
            width: nextWidth,
            height: nextHeight,
            rotation: node.rotation(),
          }
        : design,
    )
    commitDesigns(nextDesigns, id)
  }

  const handleDeleteSelected = () => {
    if (selectedId) {
      const nextTexts = texts.filter((item) => item.id !== selectedId)
      const nextSelectedId = nextTexts[0]?.id ?? null
      commitTexts(nextTexts, nextSelectedId)
      return
    }
    if (selectedDesignId) {
      const nextDesigns = designElements.filter((item) => item.id !== selectedDesignId)
      commitDesigns(nextDesigns, null)
    }
  }

  const handleUndo = () => {
    setHistory((prev) => {
      if (prev.length <= 1) return prev
      const nextHistory = prev.slice(0, -1)
      const previousState = nextHistory[nextHistory.length - 1]
      const previousTexts = previousState.texts ?? []
      const previousDesigns = previousState.designs ?? []
      const fallbackSelectedTextId =
        previousTexts.find((item) => item.id === selectedId)?.id ??
        previousTexts[0]?.id ??
        null
      const fallbackSelectedDesignId =
        previousDesigns.find((item) => item.id === selectedDesignId)?.id ??
        previousDesigns[0]?.id ??
        null

      setTexts(previousTexts)
      setDesignElements(previousDesigns)
      if (fallbackSelectedTextId) {
        setSelectedId(fallbackSelectedTextId)
        setSelectedDesignId(null)
      } else if (fallbackSelectedDesignId) {
        setSelectedId(null)
        setSelectedDesignId(fallbackSelectedDesignId)
      } else {
        setSelectedId(null)
        setSelectedDesignId(null)
      }
      return nextHistory
    })
  }

  const finalizeSelection = () => {
    if (selectedId) {
      const node = textNodeRefs.current[selectedId]
      if (node) {
        commitTransform(selectedId, node)
      }
    }
    if (selectedDesignId) {
      const node = designNodeRefs.current[selectedDesignId]
      if (node) {
        commitDesignTransform(selectedDesignId, node)
      }
    }
  }

  const captureStageDataUrl = (mode, pixelRatio, resetView = false) =>
    new Promise((resolve) => {
      const stage = stageRef.current
      if (!stage) {
        resolve('')
        return
      }
      setIsExporting(true)
      setExportMode(mode)
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          const originalScale = resetView ? { x: stage.scaleX(), y: stage.scaleY() } : null
          const originalPos = resetView ? stage.position() : null
          if (resetView) {
            stage.scale({ x: 1, y: 1 })
            stage.position({ x: 0, y: 0 })
            stage.batchDraw()
          }
          if (mode === 'print') {
            const designLayer = stage.findOne('.export-design')
            const width = 1000
            const height = 1500
            const canvas = document.createElement('canvas')
            canvas.width = width
            canvas.height = height
            const ctx = canvas.getContext('2d')
            if (ctx) {
              ctx.fillStyle = '#ffffff'
              ctx.fillRect(0, 0, width, height)
              if (designLayer) {
                const designCanvas = designLayer.toCanvas({ pixelRatio })
                const scaleX = width / (stage.width() * pixelRatio)
                const scaleY = height / (stage.height() * pixelRatio)
                ctx.drawImage(
                  designCanvas,
                  0,
                  0,
                  designCanvas.width * scaleX,
                  designCanvas.height * scaleY,
                )
              }
            }
            const dataUrl = canvas.toDataURL('image/png')
            if (resetView && originalScale && originalPos) {
              stage.scale(originalScale)
              stage.position(originalPos)
              stage.batchDraw()
            }
            setIsExporting(false)
            setExportMode('none')
            resolve(dataUrl)
            return
          }

          const dataUrl = stage?.toDataURL({ pixelRatio }) ?? ''
          if (resetView && originalScale && originalPos) {
            stage.scale(originalScale)
            stage.position(originalPos)
            stage.batchDraw()
          }

          setIsExporting(false)
          setExportMode('none')
          resolve(dataUrl)
        })
      })
    })

  const capturePreview = async () => {
    const dataUrl = await captureStageDataUrl('preview', 3)
    if (dataUrl) setPreviewDataUrl(dataUrl)
  }

  const capturePreviewForOrder = () => captureStageDataUrl('preview', 3, true)

  const capturePrintForOrder = () => captureStageDataUrl('print', printPixelRatio, true)


  const handleOpenPreview = () => {
    if (activeTab === 'preview') return
    setActiveTab('preview')
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        capturePreview()
      })
    })
  }

  const handleOpenEdit = () => {
    if (activeTab === 'edit') return
    setActiveTab('edit')
  }

  const handleCheckoutFieldChange = (field, value) => {
    setCheckoutForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleOpenCheckout = () => {
    setCheckoutError('')
    setCheckoutSuccess(null)
    setCheckoutForm((prev) => ({
      ...prev,
      magsafe: caseType?.has_magsafe ?? false,
    }))
    setIsCheckoutOpen(true)
  }

  const handleCloseCheckout = () => {
    if (isCheckoutSubmitting) return
    setIsCheckoutOpen(false)
  }

  const buildCustomizationPayload = (previewUrl, printUrl) => ({
    preview_data_url: previewUrl || previewDataUrl || null,
    print_data_url: printUrl || null,
    texts: texts.map((item) => ({
      id: item.id,
      text: item.text,
      x: item.x,
      y: item.y,
      fontSize: item.fontSize ?? 22,
      fontFamily: item.fontFamily ?? 'Itim',
      fontStyle: item.fontStyle ?? 'normal',
      align: item.align ?? 'center',
      rotation: item.rotation ?? 0,
      color: item.color,
      letterSpacing: item.letterSpacing ?? 0,
      opacity: item.opacity ?? 1,
    })),
    designs: designElements.map((item) => ({
      id: item.id,
      src: item.src,
      x: item.x,
      y: item.y,
      width: item.width,
      height: item.height,
      rotation: item.rotation ?? 0,
      opacity: item.opacity ?? 1,
    })),
    template: template
      ? {
          id: template.id,
          base_image_url: template.base_image_url,
          overlay_image_url: template.overlay_image_url,
          print_mask_url: template.print_mask_url,
          width_px: template.width_px,
          height_px: template.height_px,
          dpi: template.dpi,
        }
      : null,
  })

  const handleCheckoutSubmit = async (event) => {
    event.preventDefault()
    if (!phoneCase?.id || !phoneModel || !caseType) {
      setCheckoutError('Please select a case before checking out.')
      return
    }

    if (!checkoutForm.name.trim() || !checkoutForm.email.trim()) {
      setCheckoutError('Name and email are required.')
      return
    }

    setCheckoutError('')
    setIsCheckoutSubmitting(true)
    try {
      finalizeSelection()
      const previewUrl = await capturePreviewForOrder()
      const printUrl = await capturePrintForOrder()
      const previewImageUrl = previewUrl && previewUrl.startsWith('http') ? previewUrl : null
      const orderPayload = {
        orderer_name: checkoutForm.name.trim(),
        orderer_email: checkoutForm.email.trim(),
        orderer_phone: checkoutForm.phone.trim() || null,
        shipping_address: checkoutForm.address.trim() || null,
        shipping_postal_code: checkoutForm.postal.trim() || null,
        customization_json: buildCustomizationPayload(previewUrl, printUrl),
        preview_image_url: previewImageUrl,
      }

      const response = await fetch(`${API_BASE}/orders/create-order`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone_payload: {
            brand: phoneModel.brand,
            model_name: phoneModel.model_name,
          },
          case_payload: {
            type_name: caseType.type_name,
            description: caseType.description ?? null,
            has_magsafe: checkoutForm.magsafe,
            is_double_layer: caseType.is_double_layer ?? false,
          },
          phone_case_payload: {
            phone_model_id: phoneCase.phone_model_id,
            case_type_id: phoneCase.case_type_id,
            sku: phoneCase.sku ?? null,
            price: phoneCase.price ?? null,
          },
          template_payload: template
            ? {
                phone_case_id: phoneCase.id,
                base_image_url: template.base_image_url,
                print_mask_url: template.print_mask_url,
                overlay_image_url: template.overlay_image_url ?? null,
                width_px: template.width_px,
                height_px: template.height_px,
                dpi: template.dpi,
                bleed_mm: template.bleed_mm ?? null,
                safe_mm: template.safe_mm ?? null,
              }
            : null,
          order_payload: orderPayload,
        }),
      })

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => null)
        let message = 'Checkout failed.'
        if (errorPayload) {
          if (typeof errorPayload.message === 'string') {
            message = errorPayload.message
          } else if (Array.isArray(errorPayload.results) && errorPayload.results.length) {
            message = errorPayload.results
              .map((item) => {
                const path = Array.isArray(item.path) ? item.path.join('.') : ''
                return path ? `${path}: ${item.message}` : item.message
              })
              .join(' | ')
          } else if (errorPayload.detail) {
            message =
              typeof errorPayload.detail === 'string'
                ? errorPayload.detail
                : errorPayload.detail?.message || message
          }
        }
        throw new Error(message)
      }

      const data = await response.json()
      setCheckoutSuccess({
        orderNumber: data?.result?.order_number || data?.result?.order?.order_number || 'Created',
      })
    } catch (err) {
      setCheckoutError(err?.message || 'Checkout failed.')
    } finally {
      setIsCheckoutSubmitting(false)
    }
  }

  useEffect(() => {
    if (!template?.base_image_url) {
      setBaseImage(null)
      return
    }

    const image = new window.Image()
    image.crossOrigin = 'anonymous'
    image.src = template.base_image_url
    image.onload = () => setBaseImage(image)
  }, [template?.base_image_url])

  useEffect(() => {
    if (!template?.overlay_image_url) {
      setOverlayImage(null)
      return
    }

    const image = new window.Image()
    image.crossOrigin = 'anonymous'
    image.src = template.overlay_image_url
    image.onload = () => setOverlayImage(image)
  }, [template?.overlay_image_url])

  useEffect(() => {
    if (!template?.print_mask_url) {
      setMaskImage(null)
      return
    }

    const image = new window.Image()
    image.crossOrigin = 'anonymous'
    image.src = template.print_mask_url
    image.onload = () => setMaskImage(image)
  }, [template?.print_mask_url])

  useEffect(() => {
    const sourceImage = maskImage ?? baseImage

    if (!sourceImage) {
      setCaseBounds(null)
      setCameraBounds(null)
      return
    }

    const imageWidth = sourceImage.naturalWidth || sourceImage.width
    const imageHeight = sourceImage.naturalHeight || sourceImage.height
    if (!imageWidth || !imageHeight) return

    const canvas = document.createElement('canvas')
    canvas.width = imageWidth
    canvas.height = imageHeight
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.drawImage(sourceImage, 0, 0, imageWidth, imageHeight)
    const { data, width, height } = ctx.getImageData(0, 0, imageWidth, imageHeight)

    let minX = width
    let minY = height
    let maxX = 0
    let maxY = 0
    let hasPixel = false

    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const alpha = data[(y * width + x) * 4 + 3]
        if (alpha > 10) {
          hasPixel = true
          if (x < minX) minX = x
          if (y < minY) minY = y
          if (x > maxX) maxX = x
          if (y > maxY) maxY = y
        }
      }
    }

    if (!hasPixel) {
      setCaseBounds(null)
      setCameraBounds(null)
      return
    }

    const scaleX = stageWidth / imageWidth
    const scaleY = stageHeight / imageHeight
    const nextCaseBounds = {
      x: minX * scaleX,
      y: minY * scaleY,
      width: (maxX - minX) * scaleX,
      height: (maxY - minY) * scaleY,
    }
    setCaseBounds(nextCaseBounds)

    if (!maskImage) {
      setCameraBounds(null)
      return
    }

    const alphaThreshold = 10
    const total = width * height
    const outside = new Uint8Array(total)
    const holeVisited = new Uint8Array(total)
    const stack = []

    const pushIfOutside = (x, y) => {
      const index = y * width + x
      if (outside[index]) return
      if (data[index * 4 + 3] > alphaThreshold) return
      outside[index] = 1
      stack.push(index)
    }

    for (let x = 0; x < width; x += 1) {
      pushIfOutside(x, 0)
      pushIfOutside(x, height - 1)
    }
    for (let y = 0; y < height; y += 1) {
      pushIfOutside(0, y)
      pushIfOutside(width - 1, y)
    }

    while (stack.length) {
      const index = stack.pop()
      const x = index % width
      const y = Math.floor(index / width)

      if (x > 0) pushIfOutside(x - 1, y)
      if (x < width - 1) pushIfOutside(x + 1, y)
      if (y > 0) pushIfOutside(x, y - 1)
      if (y < height - 1) pushIfOutside(x, y + 1)
    }

    let bestArea = 0
    let bestBounds = null

    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const index = y * width + x
        if (outside[index]) continue
        if (holeVisited[index]) continue
        if (data[index * 4 + 3] > alphaThreshold) continue

        let minHoleX = x
        let minHoleY = y
        let maxHoleX = x
        let maxHoleY = y
        let area = 0
        const holeStack = [index]
        holeVisited[index] = 1

        while (holeStack.length) {
          const holeIndex = holeStack.pop()
          const hx = holeIndex % width
          const hy = Math.floor(holeIndex / width)
          area += 1

          if (hx < minHoleX) minHoleX = hx
          if (hy < minHoleY) minHoleY = hy
          if (hx > maxHoleX) maxHoleX = hx
          if (hy > maxHoleY) maxHoleY = hy

          const neighbors = [
            holeIndex - 1,
            holeIndex + 1,
            holeIndex - width,
            holeIndex + width,
          ]

          neighbors.forEach((neighbor) => {
            if (neighbor < 0 || neighbor >= total) return
            if (holeVisited[neighbor]) return
            if (outside[neighbor]) return
            if (data[neighbor * 4 + 3] > alphaThreshold) return
            holeVisited[neighbor] = 1
            holeStack.push(neighbor)
          })
        }

        if (area > bestArea) {
          bestArea = area
          bestBounds = { minHoleX, minHoleY, maxHoleX, maxHoleY }
        }
      }
    }

    if (!bestBounds || bestArea < width * height * 0.0005) {
      setCameraBounds(null)
      return
    }

    setCameraBounds({
      x: bestBounds.minHoleX * scaleX,
      y: bestBounds.minHoleY * scaleY,
      width: (bestBounds.maxHoleX - bestBounds.minHoleX) * scaleX,
      height: (bestBounds.maxHoleY - bestBounds.minHoleY) * scaleY,
    })
  }, [baseImage, maskImage, stageWidth, stageHeight])

  useEffect(() => {
    if (!overlayImage) {
      setOverlayDraw(null)
      return
    }

    const imageWidth = overlayImage.naturalWidth || overlayImage.width
    const imageHeight = overlayImage.naturalHeight || overlayImage.height
    if (!imageWidth || !imageHeight) {
      setOverlayDraw(null)
      return
    }

    const canvas = document.createElement('canvas')
    canvas.width = imageWidth
    canvas.height = imageHeight
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.drawImage(overlayImage, 0, 0, imageWidth, imageHeight)
    const { data, width, height } = ctx.getImageData(0, 0, imageWidth, imageHeight)

    let minX = width
    let minY = height
    let maxX = 0
    let maxY = 0
    let hasPixel = false

    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        const alpha = data[(y * width + x) * 4 + 3]
        if (alpha > 10) {
          hasPixel = true
          if (x < minX) minX = x
          if (y < minY) minY = y
          if (x > maxX) maxX = x
          if (y > maxY) maxY = y
        }
      }
    }

    if (!hasPixel) {
      setOverlayDraw({ x: 0, y: 0, width: stageWidth, height: stageHeight })
      return
    }

    if (!caseBounds) {
      setOverlayDraw(null)
      return
    }

    const overlayWidth = maxX - minX
    const overlayHeight = maxY - minY
    const scaleX = caseBounds.width / overlayWidth
    const scaleY = caseBounds.height / overlayHeight
    setOverlayDraw({
      x: caseBounds.x - minX * scaleX,
      y: caseBounds.y - minY * scaleY,
      width: imageWidth * scaleX,
      height: imageHeight * scaleY,
    })
  }, [overlayImage, caseBounds, stageWidth, stageHeight])

  useEffect(() => {
    const handleKeyDown = (event) => {
      const target = event.target
      const tagName = target?.tagName
      const isEditableTarget =
        target?.isContentEditable || tagName === 'INPUT' || tagName === 'TEXTAREA' || tagName === 'SELECT'

      if (editingTextId || editingBox || isEditableTarget) return
      if (!selectedId && !selectedDesignId) return
      const hasModifier = event.ctrlKey || event.metaKey
      if (hasModifier && event.key.toLowerCase() === 'd') {
        event.preventDefault()
        duplicateSelected()
        return
      }
      if (event.key === 'Delete' || event.key === 'Backspace') {
        event.preventDefault()
        handleDeleteSelected()
        return
      }
      const step = event.shiftKey ? 10 : 1
      if (event.key === 'ArrowLeft') {
        event.preventDefault()
        nudgeSelected(-step, 0)
        return
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        nudgeSelected(step, 0)
        return
      }
      if (event.key === 'ArrowUp') {
        event.preventDefault()
        nudgeSelected(0, -step)
        return
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault()
        nudgeSelected(0, step)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [selectedId, selectedDesignId, texts, designElements, editingTextId, editingBox])

  useEffect(() => {
    const transformer = transformerRef.current
    if (!transformer) return
    const node = selectedId
      ? textNodeRefs.current[selectedId]
      : selectedDesignId
        ? designNodeRefs.current[selectedDesignId]
        : null
    if (node) {
      transformer.nodes([node])
      transformer.moveToTop()
      transformer.getLayer()?.batchDraw()
    } else {
      transformer.nodes([])
      transformer.getLayer()?.batchDraw()
    }
  }, [selectedId, selectedDesignId, texts, designElements])

  const closePanels = () => {
    setIsTextLibraryOpen(false)
    setIsColorPaletteOpen(false)
    setIsDesignsOpen(false)
    setIsArtworkOpen(false)
  }

  const handleWorkspacePointerDown = (event) => {
    const target = event.target
    if (!(target instanceof Element)) return
    if (target.closest('.editor-sidebar')) return
    closePanels()
  }

  const handleStagePointerDown = (event) => {
    const target = event.target
    if (!target) return
    const targetId = typeof target.id === 'function' ? target.id() : ''
    const isDesign = targetId?.startsWith('design-')
    const isText = targetId?.startsWith('text-')
    const isTransformerHandle = target.getParent?.()?.className === 'Transformer'
    if (isDesign || isText || isTransformerHandle) return
    closePanels()
    clearSelection()
  }

  const clearSelection = () => {
    setSelectedId(null)
    setSelectedDesignId(null)
  }

  return (
    <section
      className="customization-page"
      onMouseDown={handleWorkspacePointerDown}
      onTouchStart={handleWorkspacePointerDown}
    >
      <div className="customization-layout">
        <aside className="editor-sidebar">
          <div className="editor-logo">Your Way</div>
          <button
            className="editor-action"
            type="button"
            onClick={() => uploadInputRef.current?.click()}
          >
              <span className="editor-upload-icon">⬆</span>
            <span>Upload</span>
          </button>
          <input
            ref={uploadInputRef}
            type="file"
            accept="image/*"
            multiple
            onChange={handleUploadDesigns}
            style={{ display: 'none' }}
          />
          <button className="editor-action" type="button" onClick={onBack}>
            ←
            <span>Back</span>
          </button>
          <button className="editor-action" type="button" onClick={handleOpenCheckout}>
            ✓
            <span>Checkout</span>
          </button>
          <div className="editor-section">
            <h3>Actions</h3>
            <div className="editor-pill-group">
              <button type="button" onClick={handleUndo} disabled={history.length <= 1}>
                Undo
              </button>
              <button type="button" onClick={duplicateSelected} disabled={!selectedId && !selectedDesignId}>
                Duplicate
              </button>
              <button type="button" onClick={handleDeleteSelected} disabled={!selectedId && !selectedDesignId}>
                Delete selected
              </button>
            </div>
          </div>
          <div className="editor-section">
            <button
              type="button"
              className={`editor-section-toggle ${isTextLibraryOpen ? 'is-open' : ''}`}
              onClick={() => handleTogglePanel('library')}
              aria-expanded={isTextLibraryOpen}
            >
              Text Library
              <span className="editor-toggle-icon">▾</span>
            </button>
            {isTextLibraryOpen ? (
              <div className="editor-library editor-panel editor-panel-animated">
                {textStyleGroups.map((group) => (
                  <div key={group.id} className="editor-library-group">
                    <p className="editor-library-title">{group.title}</p>
                    <div className="editor-library-grid">
                      {group.items.map((style) => (
                        <button
                          key={style.id}
                          type="button"
                          className="editor-text-sample"
                          style={{
                            fontFamily: style.fontFamily,
                            fontStyle: style.fontStyle ?? 'normal',
                            color: '#000',
                          }}
                          onClick={() => handleAddText(style)}
                        >
                          {style.label}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
          <div className="editor-section">
            <button
              type="button"
              className={`editor-section-toggle ${isDesignsOpen ? 'is-open' : ''}`}
              aria-expanded={isDesignsOpen}
              onClick={() => handleTogglePanel('designs')}
            >
              Text designs
              <span className="editor-toggle-icon">▾</span>
            </button>
            {isDesignsOpen ? (
              <div className="editor-design-grid editor-panel editor-panel-scroll editor-panel-animated">
                {textDesignItems.map((design) => (
                  <button
                    key={design.id}
                    type="button"
                    className="editor-design-card"
                    onClick={() => handleAddDesign(design.src)}
                  >
                    <img src={design.src} alt={design.name} />
                  </button>
                ))}
              </div>
            ) : null}
          </div>
          <div className="editor-section">
            <button
              type="button"
              className={`editor-section-toggle ${isArtworkOpen ? 'is-open' : ''}`}
              aria-expanded={isArtworkOpen}
              onClick={() => handleTogglePanel('artwork')}
            >
              Designs
              <span className="editor-toggle-icon">▾</span>
            </button>
            {isArtworkOpen ? (
              <div className="editor-design-grid editor-panel editor-panel-scroll editor-panel-animated">
                {artworkDesignItems.map((design) => (
                  <button
                    key={design.id}
                    type="button"
                    className="editor-design-card"
                    onClick={() => handleAddDesign(design.src)}
                  >
                    <img src={design.src} alt={design.name} />
                  </button>
                ))}
              </div>
            ) : null}
          </div>
          <div className="editor-section">
            <h3>Edit text</h3>
            <input
              className="editor-input"
              type="text"
              placeholder="Select text on the case"
              value={selectedText?.text ?? ''}
              onChange={(event) => handleTextChange(event.target.value)}
              disabled={!selectedId}
            />
          </div>
          <div className="editor-section">
            <button
              type="button"
              className={`editor-section-toggle ${isColorPaletteOpen ? 'is-open' : ''}`}
              onClick={() => handleTogglePanel('color')}
              aria-expanded={isColorPaletteOpen}
            >
              Text color
              <span className="editor-toggle-icon">▾</span>
            </button>
            {isColorPaletteOpen ? (
              <div className="editor-color-grid editor-panel editor-panel-animated">
                {colorOptions.map((color) => (
                  <button
                    key={color}
                    type="button"
                    className={`editor-color ${selectedText?.color === color ? 'is-active' : ''}`}
                    style={{ background: color }}
                    onClick={() => handleColorChange(color)}
                    aria-label={`Select ${color}`}
                  />
                ))}
              </div>
            ) : null}
          </div>
        </aside>

        <div className="editor-canvas-area">
          <div className="editor-topbar">
            {selectedText ? (
              <div className="editor-text-toolbar">
                <div className="toolbar-group">
                  <select
                    className="toolbar-select"
                    value={selectedText.fontFamily ?? 'Itim'}
                    onChange={(event) => handleFontFamilyChange(event.target.value)}
                  >
                    {fontOptions.map((font) => (
                      <option key={font.value} value={font.value}>
                        {font.label}
                      </option>
                    ))}
                  </select>
                  <input
                    className="toolbar-size"
                    type="number"
                    min={minTextFontSize}
                    max={96}
                    value={selectedText.fontSize ?? 22}
                    onChange={(event) => handleFontSizeInput(event.target.value)}
                  />
                </div>
                <div className="toolbar-group">
                  <button
                    type="button"
                    className={`toolbar-btn ${isSelectedTextBold ? 'is-active' : ''}`}
                    onClick={handleToggleBold}
                  >
                    Bold
                  </button>
                  <button
                    type="button"
                    className={`toolbar-btn ${isSelectedTextItalic ? 'is-active' : ''}`}
                    onClick={handleToggleItalic}
                  >
                    Italic
                  </button>
                  <button
                    type="button"
                    className={`toolbar-btn ${(selectedText.align ?? 'center') === 'left' ? 'is-active' : ''}`}
                    onClick={() => handleAlignChange('left')}
                  >
                    Left
                  </button>
                  <button
                    type="button"
                    className={`toolbar-btn ${(selectedText.align ?? 'center') === 'center' ? 'is-active' : ''}`}
                    onClick={() => handleAlignChange('center')}
                  >
                    Center
                  </button>
                  <button
                    type="button"
                    className={`toolbar-btn ${(selectedText.align ?? 'center') === 'right' ? 'is-active' : ''}`}
                    onClick={() => handleAlignChange('right')}
                  >
                    Right
                  </button>
                </div>
                <div className="toolbar-group toolbar-group-range">
                  <span className="toolbar-mini-label">Spacing</span>
                  <input
                    className="toolbar-range"
                    type="range"
                    min={0}
                    max={12}
                    step={0.5}
                    value={selectedText.letterSpacing ?? 0}
                    onChange={(event) => handleLetterSpacingChange(event.target.value)}
                  />
                </div>
                <div className="toolbar-group toolbar-group-range">
                  <span className="toolbar-mini-label">Opacity</span>
                  <input
                    className="toolbar-range"
                    type="range"
                    min={0.15}
                    max={1}
                    step={0.01}
                    value={selectedElementOpacity}
                    onChange={(event) => handleElementOpacityChange(event.target.value)}
                  />
                </div>
                <button type="button" className="toolbar-btn" onClick={duplicateSelected}>
                  Duplicate
                </button>
                <button type="button" className="toolbar-delete" onClick={handleDeleteSelected}>
                  Delete
                </button>
              </div>
            ) : selectedDesign ? (
              <div className="editor-text-toolbar">
                <div className="toolbar-group toolbar-group-range">
                  <span className="toolbar-mini-label">Design opacity</span>
                  <input
                    className="toolbar-range"
                    type="range"
                    min={0.15}
                    max={1}
                    step={0.01}
                    value={selectedElementOpacity}
                    onChange={(event) => handleElementOpacityChange(event.target.value)}
                  />
                </div>
                <button type="button" className="toolbar-btn" onClick={duplicateSelected}>
                  Duplicate
                </button>
                <button type="button" className="toolbar-delete" onClick={handleDeleteSelected}>
                  Delete
                </button>
              </div>
            ) : null}
            <div className="editor-zoom-controls">
              <button
                type="button"
                className="editor-zoom-btn"
                onClick={() => setZoom((value) => Math.max(0.5, Number((value - 0.05).toFixed(3))))}
              >
                −
              </button>
              <span className="editor-zoom-label">{Math.round(zoom * 100)}%</span>
              <button
                type="button"
                className="editor-zoom-btn"
                onClick={() => setZoom((value) => Math.min(2, Number((value + 0.05).toFixed(3))))}
              >
                +
              </button>
            </div>
            <button
              type="button"
              className={`editor-tab ${activeTab === 'edit' ? 'is-active' : ''}`}
              onClick={handleOpenEdit}
            >
              Edit
            </button>
            <button
              type="button"
              className={`editor-tab ${activeTab === 'preview' ? 'is-active' : ''}`}
              onClick={handleOpenPreview}
            >
              Preview
            </button>
            <button type="button" className="editor-checkout" onClick={handleOpenCheckout}>
              Checkout
            </button>
          </div>
          <div className="editor-canvas" ref={editorCanvasRef}>
            {!hasTemplateAssets ? (
              <div className="editor-empty">No template data found for this case.</div>
            ) : !isTemplateReady ? (
              <div className="editor-empty">Waiting for template images...</div>
            ) : (
              <>
                <div className={`editor-stage ${isPreviewMode ? 'is-hidden' : ''}`}>
                  <Stage
                    ref={stageRef}
                    width={stageWidth}
                    height={stageHeight}
                    scaleX={zoom}
                    scaleY={zoom}
                    onMouseDown={handleStagePointerDown}
                    onTouchStart={handleStagePointerDown}
                  >
                    <Layer>
                      <Rect
                        name="export-bg"
                        x={0}
                        y={0}
                        width={stageWidth}
                        height={stageHeight}
                        fill={stageBackground}
                      />
                      {!isPrintExport && caseBounds ? (
                        <Rect
                          x={caseBounds.x}
                          y={caseBounds.y}
                          width={caseBounds.width}
                          height={caseBounds.height}
                          fillPatternImage={dotPatternImage}
                          fillPatternRepeat="repeat"
                          opacity={0.3}
                          listening={false}
                        />
                      ) : null}
                    </Layer>
                    {!isPreviewMode && !isPrintExport && maskImage ? (
                      <Layer name="export-hide">
                        <Rect x={0} y={0} width={stageWidth} height={stageHeight} fill="#ffffff" />
                        <KonvaImage
                          image={maskImage}
                          x={0}
                          y={0}
                          width={stageWidth}
                          height={stageHeight}
                          globalCompositeOperation="destination-in"
                          listening={false}
                        />
                      </Layer>
                    ) : null}
                    {baseImage && !isPrintExport && showBaseImage ? (
                      <Layer name="export-hide">
                        <KonvaImage
                          image={baseImage}
                          x={0}
                          y={0}
                          width={stageWidth}
                          height={stageHeight}
                          listening={false}
                        />
                      </Layer>
                    ) : null}
                    <Layer name="export-design">
                      {designElements.map((item) => (
                        <KonvaImage
                          key={item.id}
                          id={`design-${item.id}`}
                          image={item.image}
                          x={item.x}
                          y={item.y}
                          width={item.width}
                          height={item.height}
                          rotation={item.rotation ?? 0}
                          zIndex={item.zIndex ?? 0}
                          draggable
                          ref={(node) => {
                            if (node) {
                              designNodeRefs.current[item.id] = node
                            }
                          }}
                          onMouseDown={() => {
                            setSelectedDesignId(item.id)
                            setSelectedId(null)
                          }}
                          onTouchStart={() => {
                            setSelectedDesignId(item.id)
                            setSelectedId(null)
                          }}
                          onDragEnd={(event) => {
                            const nextPosition = event.target.position()
                            const nextDesigns = designElements.map((design) =>
                              design.id === item.id ? { ...design, ...nextPosition } : design,
                            )
                            commitDesigns(nextDesigns, item.id)
                          }}
                          opacity={item.opacity ?? 1}
                        />
                      ))}
                      {texts.map((item) => (
                        <Text
                          key={item.id}
                          id={`text-${item.id}`}
                          text={item.text}
                          x={item.x}
                          y={item.y}
                          fontSize={item.fontSize ?? 22}
                          fontFamily={item.fontFamily ?? 'Itim'}
                          fontStyle={item.fontStyle ?? 'normal'}
                          align={item.align ?? 'center'}
                          width={item.width ?? defaultTextBoxWidth}
                          letterSpacing={item.letterSpacing ?? 0}
                          rotation={item.rotation ?? 0}
                          fill={item.color}
                          stroke={(item.fontStyle ?? '').includes('bold') ? item.color : undefined}
                          strokeWidth={(item.fontStyle ?? '').includes('bold') ? Math.max(0.6, (item.fontSize ?? 22) * 0.04) : 0}
                          skewX={(item.fontStyle ?? '').includes('italic') ? -0.22 : 0}
                          zIndex={item.zIndex ?? 0}
                          draggable
                          ref={(node) => {
                            if (node) {
                              textNodeRefs.current[item.id] = node
                            }
                          }}
                          onMouseDown={() => {
                            setSelectedId(item.id)
                            setSelectedDesignId(null)
                          }}
                          onTouchStart={() => {
                            setSelectedId(item.id)
                            setSelectedDesignId(null)
                          }}
                          onDragEnd={(event) => handleDragEnd(item.id, event)}
                          onClick={() => {
                            setSelectedId(item.id)
                            setSelectedDesignId(null)
                          }}
                          onDblClick={() => startInlineTextEdit(item.id)}
                          onTap={() => {
                            setSelectedId(item.id)
                            setSelectedDesignId(null)
                          }}
                          onDblTap={() => startInlineTextEdit(item.id)}
                          opacity={item.opacity ?? 1}
                        />
                      ))}
                    </Layer>
                    {!isPreviewMode ? (
                      <Layer listening={false} name="export-hide">
                        {maskImage ? (
                          <>
                            <Rect
                              x={0}
                              y={0}
                              width={stageWidth}
                              height={stageHeight}
                              fill="rgba(90, 90, 90, 0.45)"
                            />
                            <KonvaImage
                              image={maskImage}
                              x={0}
                              y={0}
                              width={stageWidth}
                              height={stageHeight}
                              globalCompositeOperation="destination-out"
                            />
                          </>
                        ) : caseBounds ? (
                          <>
                            <Rect
                              x={0}
                              y={0}
                              width={stageWidth}
                              height={Math.max(0, caseBounds.y)}
                              fill="rgba(90, 90, 90, 0.45)"
                            />
                            <Rect
                              x={0}
                              y={caseBounds.y}
                              width={Math.max(0, caseBounds.x)}
                              height={caseBounds.height}
                              fill="rgba(90, 90, 90, 0.45)"
                            />
                            <Rect
                              x={caseBounds.x + caseBounds.width}
                              y={caseBounds.y}
                              width={Math.max(0, stageWidth - (caseBounds.x + caseBounds.width))}
                              height={caseBounds.height}
                              fill="rgba(90, 90, 90, 0.45)"
                            />
                            <Rect
                              x={0}
                              y={caseBounds.y + caseBounds.height}
                              width={stageWidth}
                              height={Math.max(0, stageHeight - (caseBounds.y + caseBounds.height))}
                              fill="rgba(90, 90, 90, 0.45)"
                            />
                          </>
                        ) : null}
                      </Layer>
                    ) : null}
                    {(overlayImage && !isPrintExport) || !isPreviewMode ? (
                      <Layer name="export-hide">
                        {overlayImage && !isPrintExport ? (
                          <KonvaImage
                            image={overlayImage}
                            x={maskImage ? 0 : overlayDraw?.x ?? 0}
                            y={maskImage ? 0 : overlayDraw?.y ?? 0}
                            width={maskImage ? stageWidth : overlayDraw?.width ?? stageWidth}
                            height={maskImage ? stageHeight : overlayDraw?.height ?? stageHeight}
                            listening={false}
                          />
                        ) : null}
                        {!isPreviewMode ? (
                          <>
                            {caseBounds ? (
                              <>
                                <Rect
                                  x={caseBounds.x + safeInset}
                                  y={caseBounds.y + safeInset}
                                  width={caseBounds.width - safeInset * 2}
                                  height={caseBounds.height - safeInset * 2}
                                  stroke="#c8b29b"
                                  dash={[0.1, 7]}
                                  strokeWidth={2}
                                  lineCap="round"
                                  strokeOpacity={0.9}
                                  cornerRadius={Math.min(
                                    caseBounds.width - safeInset * 2,
                                    caseBounds.height - safeInset * 2,
                                  ) * 0.08}
                                  listening={false}
                                />
                                {cameraBounds ? (
                                  <Rect
                                    x={cameraBounds.x}
                                    y={cameraBounds.y}
                                    width={cameraBounds.width}
                                    height={cameraBounds.height}
                                    stroke="#c8b29b"
                                    dash={[0.1, 7]}
                                    strokeWidth={2}
                                    lineCap="round"
                                    strokeOpacity={0.9}
                                    cornerRadius={Math.min(cameraBounds.width, cameraBounds.height) * 0.25}
                                    listening={false}
                                  />
                                ) : null}
                              </>
                            ) : null}
                            <Transformer
                              ref={transformerRef}
                              rotateEnabled
                              onTransformEnd={() => {
                                const node = transformerRef.current?.nodes?.()[0]
                                if (!node) return
                                const nodeId = node.id()
                                if (nodeId?.startsWith('text-')) {
                                  const actualId = nodeId.replace('text-', '')
                                  commitTransform(actualId, node)
                                  return
                                }
                                if (nodeId?.startsWith('design-')) {
                                  const actualId = nodeId.replace('design-', '')
                                  commitDesignTransform(actualId, node)
                                }
                              }}
                              enabledAnchors={['top-left', 'top-right', 'bottom-left', 'bottom-right']}
                              anchorSize={12}
                              anchorCornerRadius={4}
                              anchorFill="#ffffff"
                              anchorStroke="#7a5a2b"
                              anchorStrokeWidth={1.5}
                              borderStroke="#7a5a2b"
                              borderStrokeWidth={1.5}
                              borderDash={[6, 4]}
                              padding={8}
                              boundBoxFunc={(oldBox, newBox) => {
                                const activeNode = transformerRef.current?.nodes?.()[0]
                                const activeNodeId = activeNode?.id?.() ?? ''
                                const minSize = activeNodeId.startsWith('text-') ? 12 : 24
                                if (newBox.width < minSize || newBox.height < minSize) return oldBox
                                return newBox
                              }}
                            />
                          </>
                        ) : null}
                      </Layer>
                    ) : null}
                  </Stage>
                </div>
                {isPreviewMode ? (
                  <div className="editor-preview">
                    {previewDataUrl ? (
                      <div className="preview-shell">
                        <div className="preview-device">
                          <div
                            className="preview-image"
                            style={{ backgroundImage: `url(${previewDataUrl})` }}
                          />
                          <div className="preview-gloss" />
                        </div>
                        <div className="preview-shadow" />
                      </div>
                    ) : (
                      <div className="editor-empty">Preview not ready yet.</div>
                    )}
                    <p className="preview-note">3D preview of your design</p>
                  </div>
                ) : null}
              </>
            )}
          </div>
          {editingBox ? (
            <input
              ref={textEditorRef}
              className="editor-text-editor"
              style={{
                left: `${editingBox.left}px`,
                top: `${editingBox.top}px`,
                width: `${editingBox.width}px`,
                height: `${editingBox.height}px`,
              }}
              value={editingValue}
              onChange={(event) => handleInlineChange(event.target.value)}
              onBlur={() => finishInlineTextEdit(true)}
              onKeyDown={handleInlineKeyDown}
            />
          ) : null}
          <p className="editor-hint">Drag to move. Use corner handles to resize. Arrow keys nudge by 1px, Shift + arrows by 10px, Ctrl/Cmd + D duplicates.</p>
          {phoneCase ? (
            <p className="editor-case">Selected: {phoneCase.title || `Case #${phoneCase.id}`}</p>
          ) : null}
        </div>
      </div>
      {isCheckoutOpen ? (
        <div className="checkout-modal" role="dialog" aria-modal="true">
          <div className="checkout-card">
            <button
              type="button"
              className="checkout-close"
              onClick={handleCloseCheckout}
              aria-label="Close"
            >
              ×
            </button>
            <h3>Checkout</h3>
            <p className="checkout-subtitle">We will save your design with this order.</p>
            {checkoutSuccess ? (
              <div className="checkout-success">
                <h4>Order placed!</h4>
                <p>Your order number is <strong>{checkoutSuccess.orderNumber}</strong>.</p>
                <button type="button" className="checkout-btn" onClick={handleCloseCheckout}>
                  Done
                </button>
              </div>
            ) : (
              <form className="checkout-form" onSubmit={handleCheckoutSubmit}>
                <label>
                  Name
                  <input
                    type="text"
                    value={checkoutForm.name}
                    onChange={(event) => handleCheckoutFieldChange('name', event.target.value)}
                    required
                  />
                </label>
                <label>
                  Email
                  <input
                    type="email"
                    value={checkoutForm.email}
                    onChange={(event) => handleCheckoutFieldChange('email', event.target.value)}
                    required
                  />
                </label>
                <label>
                  Phone (UAE)
                  <input
                    type="tel"
                    value={checkoutForm.phone}
                    onChange={(event) => handleCheckoutFieldChange('phone', event.target.value)}
                    placeholder="+9715xxxxxxxx"
                  />
                </label>
                <label>
                  Shipping address
                  <textarea
                    rows="3"
                    value={checkoutForm.address}
                    onChange={(event) => handleCheckoutFieldChange('address', event.target.value)}
                  />
                </label>
                
                <label>
                  MagSafe
                  <select
                    value={checkoutForm.magsafe ? 'yes' : 'no'}
                    onChange={(event) =>
                      handleCheckoutFieldChange('magsafe', event.target.value === 'yes')
                    }
                  >
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                  </select>
                </label>
                {checkoutError ? <div className="checkout-error">{checkoutError}</div> : null}
                <button
                  type="submit"
                  className="checkout-btn"
                  disabled={isCheckoutSubmitting}
                >
                  {isCheckoutSubmitting ? 'Placing order...' : 'Place order'}
                </button>
              </form>
            )}
          </div>
        </div>
      ) : null}
    </section>
  )
}

const ADMIN_TOKEN_KEY = 'adminAccessToken'

const ADMIN_PATH_PREFIX = '#/admin'
const ADMIN_LOGIN_URL = `${API_BASE}/admin/admin/login`
const ADMIN_ORDERS_URL = `${API_BASE}/orders/orders`

function getAdminRouteFromHash() {
  if (typeof window === 'undefined') return null
  const hash = window.location.hash || ''
  if (!hash.startsWith(ADMIN_PATH_PREFIX)) return null
  const parts = hash.replace(ADMIN_PATH_PREFIX, '').split('/').filter(Boolean)
  if (parts.length === 0 || parts[0] === 'login') {
    return { page: 'login' }
  }
  if (parts[0] === 'orders' && parts.length === 1) {
    return { page: 'orders' }
  }
  if (parts[0] === 'orders' && parts[1]) {
    const orderId = Number(parts[1])
    return { page: 'detail', orderId: Number.isFinite(orderId) ? orderId : null }
  }
  return { page: 'login' }
}

function setAdminHash(path) {
  window.location.hash = `${ADMIN_PATH_PREFIX}${path}`
}

function AdminShell({ route, token, onLogin, onLogout, onSelectOrder, onBackToOrders }) {
  useEffect(() => {
    if (!token && route.page !== 'login') {
      setAdminHash('/login')
    }
    if (token && route.page === 'login') {
      setAdminHash('/orders')
    }
  }, [route.page, token])

  return (
    <div className="admin-shell">
      <header className="admin-header">
        <div>
          <p className="admin-eyebrow">Admin portal</p>
          <h1>Order management</h1>
        </div>
        <div className="admin-actions">
          {token ? (
            <button type="button" className="admin-btn ghost" onClick={onLogout}>
              Log out
            </button>
          ) : null}
        </div>
      </header>
      <main className="admin-body">
        {route.page === 'login' ? (
          <AdminLoginPage onLogin={onLogin} />
        ) : route.page === 'orders' ? (
          <AdminOrdersPage token={token} onSelectOrder={onSelectOrder} />
        ) : (
          <AdminOrderDetailPage
            token={token}
            orderId={route.orderId}
            onBack={onBackToOrders}
            onMarkComplete={onBackToOrders}
          />
        )}
      </main>
    </div>
  )
}

function AdminLoginPage({ onLogin }) {
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!name.trim() || !password.trim()) {
      setError('Please enter admin name and password.')
      return
    }

    try {
      setIsLoading(true)
      setError('')
      const response = await fetch(ADMIN_LOGIN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim(), password }),
      })

      if (!response.ok) {
        throw new Error('Invalid admin credentials.')
      }

      const data = await response.json()
      const token = data?.result?.access_token
      if (!token) {
        throw new Error('Missing access token.')
      }
      onLogin(token)
    } catch (err) {
      setError(err?.message || 'Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="admin-login">
      <div className="admin-card">
        <h2>Admin sign in</h2>
        <p>Access orders and update fulfillment status.</p>
        <form onSubmit={handleSubmit} className="admin-form">
          <label>
            Admin name
            <input
              type="text"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Enter admin name"
              autoComplete="username"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter password"
              autoComplete="current-password"
            />
          </label>
          {error ? <div className="admin-error">{error}</div> : null}
          <button type="submit" className="admin-btn primary" disabled={isLoading}>
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
      </div>
    </section>
  )
}

function parseCustomization(value) {
  if (!value) return null
  if (typeof value === 'string') {
    try {
      return JSON.parse(value)
    } catch (err) {
      return null
    }
  }
  return value
}

function getOrderField(order, snakeKey, camelKey) {
  if (!order) return null
  if (snakeKey in order) return order[snakeKey]
  if (camelKey && camelKey in order) return order[camelKey]
  return null
}

function AdminOrdersPage({ token, onSelectOrder }) {
  const [orders, setOrders] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)

  const fetchOrders = async () => {
    if (!token) return
    try {
      setIsLoading(true)
      setError('')
      const response = await fetch(ADMIN_ORDERS_URL, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (!response.ok) {
        throw new Error('Failed to load orders.')
      }
      const data = await response.json()
      setOrders(data?.result ?? [])
    } catch (err) {
      setError(err?.message || 'Failed to load orders.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchOrders()
  }, [token])

  const handleSearch = async (event) => {
    event.preventDefault()
    if (!query.trim()) {
      fetchOrders()
      return
    }
    try {
      setIsSearching(true)
      setError('')
      const response = await fetch(`${ADMIN_ORDERS_URL}/search/${encodeURIComponent(query.trim())}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (!response.ok) {
        throw new Error('No orders found.')
      }
      const data = await response.json()
      setOrders(data?.result ?? [])
    } catch (err) {
      setOrders([])
      setError(err?.message || 'No orders found.')
    } finally {
      setIsSearching(false)
    }
  }

  const handleToggle = async (order) => {
    try {
      const isCompleted = order.status === 'COMPLETED'
      const newStatus = isCompleted ? 'PENDING' : 'COMPLETED'
      const endpoint = isCompleted ? 'pending' : 'complete'
      
      const response = await fetch(`${ADMIN_ORDERS_URL}/${order.id}/${endpoint}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (!response.ok) {
        throw new Error('Failed to update order.')
      }
      setOrders((prev) =>
        prev.map((item) => (item.id === order.id ? { ...item, status: newStatus } : item)),
      )
    } catch (err) {
      setError(err?.message || 'Failed to update order.')
    }
  }

  return (
    <section className="admin-orders">
      <div className="admin-toolbar">
        <form className="admin-search" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search by order number"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <button type="submit" className="admin-btn" disabled={isSearching}>
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </form>
        <button type="button" className="admin-btn ghost" onClick={fetchOrders}>
          Refresh
        </button>
      </div>

      {isLoading ? <p className="admin-empty">Loading orders...</p> : null}
      {error ? <p className="admin-error">{error}</p> : null}

      {!isLoading && !error && orders.length === 0 ? (
        <p className="admin-empty">No orders found.</p>
      ) : null}

      <div className="admin-order-grid">
        {orders.map((order) => {
          const customization = parseCustomization(
            getOrderField(order, 'customization_json', 'customizationJson'),
          )
          const previewImageUrl = getOrderField(order, 'preview_image_url', 'previewImageUrl')
          const printImageUrl = getOrderField(order, 'print_image_url', 'printImageUrl')
          const previewImage =
            previewImageUrl ||
            printImageUrl ||
            customization?.preview_data_url ||
            null
          return (
            <article className="admin-order-card" key={order.id}>
              <button type="button" className="admin-order-preview" onClick={() => onSelectOrder(order.id)}>
                {previewImage ? (
                  <img src={previewImage} alt={`Order ${order.order_number}`} loading="lazy" />
                ) : (
                  <div className="admin-order-placeholder">No preview</div>
                )}
              </button>
              <div className="admin-order-meta">
                <div>
                  <p className="admin-order-number">#{order.order_number}</p>
                  <p className="admin-order-name">{order.orderer_name}</p>
                </div>
                <div className="admin-order-phone">
                  <span>{order.phone_model?.brand ?? 'Unknown brand'}</span>
                  <span>{order.phone_model?.model_name ?? 'Unknown model'}</span>
                </div>
              </div>
              <div className="admin-order-status">
                <span className={`admin-badge ${order.status === 'COMPLETED' ? 'is-complete' : 'is-pending'}`}>
                  {order.status === 'COMPLETED' ? 'Completed' : 'Pending'}
                </span>
                <label className="admin-toggle">
                  <input
                    type="checkbox"
                    checked={order.status === 'COMPLETED'}
                    onChange={() => handleToggle(order)}
                  />
                  <span className="admin-toggle-track" />
                </label>
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}

function AdminOrderDetailPage({ token, orderId, onBack }) {
  const [order, setOrder] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchOrder = async () => {
      if (!token) return
      if (!orderId) {
        setError('Invalid order.')
        setIsLoading(false)
        return
      }
      try {
        setIsLoading(true)
        setError('')
        const response = await fetch(`${ADMIN_ORDERS_URL}/${orderId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (!response.ok) {
          throw new Error('Failed to load order details.')
        }
        const data = await response.json()
        setOrder(data?.result ?? null)
      } catch (err) {
        setError(err?.message || 'Failed to load order details.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchOrder()
  }, [token, orderId])

  const customization = parseCustomization(
    getOrderField(order, 'customization_json', 'customizationJson'),
  )
  const previewImageUrl = getOrderField(order, 'preview_image_url', 'previewImageUrl')
  const printImageUrl = getOrderField(order, 'print_image_url', 'printImageUrl')
  const customPreview = previewImageUrl || printImageUrl || customization?.preview_data_url
  const designImage = customPreview || order?.template?.base_image_url
  const overlayImage = order?.template?.overlay_image_url
  const maskImage = order?.template?.print_mask_url

  const handleAdminDownload = async () => {
    const templateMeta = customization?.template || order?.template
    const targetWidth = templateMeta?.width_px
    const targetHeight = templateMeta?.height_px
    const printDataUrl = customization?.print_data_url
    const downloadImage = printDataUrl || printImageUrl || designImage
    if (!downloadImage) return

    if (printDataUrl && targetWidth && targetHeight) {
      const resizedDataUrl = await new Promise((resolve) => {
        const image = new Image()
        image.onload = () => {
          const paddingRatio = 0.2
          const canvas = document.createElement('canvas')
          canvas.width = Math.round(targetWidth * (1 + paddingRatio * 2))
          canvas.height = Math.round(targetHeight)
          const ctx = canvas.getContext('2d')
          if (!ctx) {
            resolve(printDataUrl)
            return
          }
          ctx.fillStyle = '#ffffff'
          ctx.fillRect(0, 0, canvas.width, canvas.height)
          const offsetX = Math.round(targetWidth * paddingRatio)
          const offsetY = 0
          ctx.drawImage(image, offsetX, offsetY, targetWidth, targetHeight)
          resolve(canvas.toDataURL('image/png'))
        }
        image.onerror = () => resolve(printDataUrl)
        image.src = printDataUrl
      })
      const link = document.createElement('a')
      link.href = resizedDataUrl
      link.download = `order-${order?.order_number || 'design'}.png`
      link.click()
      return
    }

    const link = document.createElement('a')
    link.href = downloadImage
    link.download = `order-${order?.order_number || 'design'}.png`
    link.click()
  }

  return (
    <section className="admin-detail">
      <div className="admin-toolbar">
        <button type="button" className="admin-btn ghost" onClick={onBack}>
          ← Back to orders
        </button>
        <button type="button" className="admin-btn" onClick={handleAdminDownload} disabled={!designImage}>
          Download design
        </button>
      </div>

      {isLoading ? <p className="admin-empty">Loading order...</p> : null}
      {error ? <p className="admin-error">{error}</p> : null}

      {!isLoading && order ? (
        <div className="admin-detail-grid">
          <div className="admin-detail-preview">
            <div className="admin-preview-stack">
              {designImage ? (
                <img src={designImage} alt="Designed case" className="admin-preview-layer is-design" />
              ) : (
                <div className="admin-order-placeholder">No design</div>
              )}
              {!customPreview && overlayImage ? (
                <img src={overlayImage} alt="Overlay" className="admin-preview-layer is-overlay" />
              ) : null}
              {!customPreview && maskImage ? (
                <img src={maskImage} alt="Mask" className="admin-preview-layer is-mask" />
              ) : null}
            </div>
          </div>
          <div className="admin-detail-card">
            <h2>Order #{order.order_number}</h2>
            <p className="admin-detail-status">
              Status:
              <span className={`admin-badge ${order.status === 'COMPLETED' ? 'is-complete' : 'is-pending'}`}>
                {order.status === 'COMPLETED' ? 'Completed' : 'Pending'}
              </span>
            </p>
            <div className="admin-detail-section">
              <h3>Customer</h3>
              <p>{order.orderer_name}</p>
              <p>{order.orderer_email}</p>
              {order.orderer_phone ? <p>{order.orderer_phone}</p> : null}
            </div>
            <div className="admin-detail-section">
              <h3>Device</h3>
              <p>{order.phone_model?.brand}</p>
              <p>{order.phone_model?.model_name}</p>
              <p>{order.case_type?.type_name}</p>
              <p>MagSafe: {order.case_type?.has_magsafe ? 'Yes' : 'No'}</p>
            </div>
            <div className="admin-detail-section">
              <h3>Shipping</h3>
              <p>{order.shipping_address || 'No shipping address'}</p>
              <p>{order.shipping_postal_code || 'No postal code'}</p>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  )
}

function App() {
  const [adminRoute, setAdminRoute] = useState(() => getAdminRouteFromHash())
  const [adminToken, setAdminToken] = useState(() => localStorage.getItem(ADMIN_TOKEN_KEY) || '')
  const [activePage, setActivePage] = useState('home')
  const [displayPage, setDisplayPage] = useState('home')
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [selectedCase, setSelectedCase] = useState(null)
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [selectedModel, setSelectedModel] = useState(null)
  const [selectedCaseType, setSelectedCaseType] = useState(null)

  useEffect(() => {
    if (activePage === displayPage) {
      return
    }

    setIsTransitioning(true)
    const timeout = setTimeout(() => {
      setDisplayPage(activePage)
      setIsTransitioning(false)
    }, 220)

    return () => clearTimeout(timeout)
  }, [activePage, displayPage])

  useEffect(() => {
    const handleHashChange = () => {
      setAdminRoute(getAdminRouteFromHash())
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  useEffect(() => {
    if (adminToken) {
      localStorage.setItem(ADMIN_TOKEN_KEY, adminToken)
    } else {
      localStorage.removeItem(ADMIN_TOKEN_KEY)
    }
  }, [adminToken])

  if (adminRoute) {
    return (
      <AdminShell
        route={adminRoute}
        token={adminToken}
        onLogin={(token) => {
          setAdminToken(token)
          setAdminHash('/orders')
        }}
        onLogout={() => {
          setAdminToken('')
          setAdminHash('/login')
        }}
        onSelectOrder={(orderId) => setAdminHash(`/orders/${orderId}`)}
        onBackToOrders={() => setAdminHash('/orders')}
      />
    )
  }

  return (
    <div className="page">
      <header className="header">
        <div className="brand">
          <img src={logo} alt="Your Way" />
        </div>
        <nav className="nav">
          <button
            type="button"
            className={`nav-pill ${activePage === 'home' ? 'is-active' : ''}`}
            onClick={() => setActivePage('home')}
          >
            <span className="nav-icon">★</span>
            Home
          </button>
          <button
            type="button"
            className={`nav-pill ${['customize', 'customize-select', 'customization'].includes(activePage) ? 'is-active' : ''}`}
            onClick={() => setActivePage('customize')}
          >
            <span className="nav-icon">★</span>
            Customize
          </button>
        </nav>
      </header>

      <div className={`page-transition ${isTransitioning ? 'is-fading' : ''}`}>
        {displayPage === 'customize' ? (
          <CustomizeLandingPage
            onSelectFromScratch={() => setActivePage('customize-select')}
          />
        ) : displayPage === 'customize-select' ? (
          <CaseCatalogPage
            title="Select a case to customize"
            subtitle="Filter by brand, model, and case type."
            actionLabel="Select"
            includeTemplates
            onBack={() => setActivePage('customize')}
            onSelectCase={(phoneCase, template, phoneModel, caseType) => {
              setSelectedCase(phoneCase)
              setSelectedTemplate(template ?? null)
              setSelectedModel(phoneModel ?? null)
              setSelectedCaseType(caseType ?? null)
              setActivePage('customization')
            }}
          />
        ) : displayPage === 'customization' ? (
          <CustomizationPage
            onBack={() => setActivePage('customize-select')}
            phoneCase={selectedCase}
            template={selectedTemplate}
            phoneModel={selectedModel}
            caseType={selectedCaseType}
          />
        ) : (
          <HomePage onStartDesigning={() => setActivePage('customize')} />
        )}
      </div>
    </div>
  )
}

export default App
