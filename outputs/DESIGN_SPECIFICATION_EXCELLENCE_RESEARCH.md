# Исследование: Мировые стандарты дизайн-спецификаций

**Дата**: 2026-01-03
**Агент**: product-manager
**Цель**: Анализ стандартов дизайн-систем мирового класса для интеграции в /speckit.design

---

## Executive Summary

Проведен анализ дизайн-систем топ-компаний (Apple, Airbnb, Uber, Stripe, Google) и индустриальных стандартов 2025 года. Выявлены 8 ключевых областей спецификаций и 47 критических чеклистов для world-class дизайн-документации.

**Ключевые находки**:
- W3C Design Tokens Specification 2025.10 — первый стабильный стандарт токенов
- WCAG 2.2 стал базовым стандартом доступности (ISO/IEC 40500:2025)
- Apple Liquid Glass (2025) — крупнейший редизайн системы с 2013 года
- Airbnb Summer 2025 — переход к 3D/скевоморфизму, команда 200+ дизайнеров
- Figma Dev Mode — новый стандарт handoff-процессов

---

## 1. Design System Excellence: Топ-компании

### 1.1 Apple Human Interface Guidelines (HIG)

**Liquid Glass Design Language (2025)** — самый масштабный редизайн ОС с 2013 года.

**Ключевые принципы**:
- **Clarity** — чистота, точность, отсутствие визуального шума
- **Consistency** — стандартные UI-элементы, предсказуемость паттернов
- **Depth** — слои, тени, motion для создания иерархии

**Спецификации**:
- Шрифт: San Francisco, базовый размер 17pt
- Touch targets: минимум 44×44pt (исследования показывают 25%+ ошибок при меньших размерах)
- Сетка: 8pt grid для консистентности между платформами
- Компоненты: единая анатомия, переиспользуемые части

**Источник**: [Apple HIG](https://developer.apple.com/design/human-interface-guidelines), [WWDC25 Design System](https://developer.apple.com/videos/play/wwdc2025/356/)

---

### 1.2 Airbnb Design Language System (DLS)

**Summer 2025 Update** — крупнейшая трансформация дизайн-системы:
- 3D, скевоморфные, Pixar-inspired иконки
- Анимации, освещение, мягкие кривые, drop-shadows
- 200-человеческая глобальная команда дизайнеров
- Полностью перестроенный tech stack для модульных компонентов

**Структура документации**:
- **Primitives** — высокоуровневые паттерны (цвет, типографика, формы)
- **Components** — контейнеры паттернов (карточки, модули)
- **Elements** — неделимые части (инпуты, лейблы)

**Governance модель**:
- Четкая модель владения компонентами
- Semantic versioning для токенов и компонентов
- Процесс контрибуций: design proposal → implementation → a11y review → release
- Кросс-функциональные рабочие группы

**Accessibility & Globalization**:
- Выделенные секции a11y и g11n в каждом компоненте
- WCAG-соответствие для контраста, screen readers, клавиатурной навигации

**Источник**: [Airbnb DLS](https://karrisaarinen.com/dls/), [Airbnb 2025 Update](https://medium.com/design-bootcamp/airbnb-summer-2025-update-heres-what-s-new-and-why-it-matters-0ced2338b921)

---

### 1.3 Uber Base Design System

**Ключевая идея**: Единый фреймворк для всех продуктов Uber (Rider, Driver, Eats, Freight, Jump).

**Design Tokens Architecture**:
- Color Tokens & Semantics — построена с нуля для масштабирования
- Light/Dark mode для всех приложений
- Typography: Uber Move, Uber Move Mono
- Grid systems: Columns, Rows

**Первопроходцы**:
- Первая DSL в Uber с **Accessibility как first-class citizen**
- Robust и scalable foundation для design at scale
- Cross-platform: Web (Base Web React), iOS, Android на одних foundational elements

**Источник**: [Base Design System](https://base.uber.com/), [Design Tokens](https://base.uber.com/6d2425e9f/p/33fa5e-design-tokens)

---

### 1.4 Stripe Design System

**UI Components & Apps**:
- Компоненты структурируют лейауты и создают интерактивный опыт
- Все компоненты доступны в Figma (@stripedesign)
- **Ограниченная кастомизация** для поддержки консистентности и accessibility bar

**View Components**:
- **ContextView** — дефолтный view приложения, рендерится рядом с Stripe-контентом в drawer
- **SettingsView** — view для настроек
- Каждый компонент должен иметь view root component

**Accessible Color System**:
- Использование perceptually uniform color model (CIELAB)
- Дефолтные цвета для текста/иконок проходят WCAG 2.0 contrast threshold
- Предсказуемое прохождение accessibility guidelines
- Консистентный визуальный вес (visual weight) между hues

**Источник**: [Stripe UI Components](https://docs.stripe.com/stripe-apps/components), [Accessible Color Systems](https://stripe.com/blog/accessible-color-systems)

---

### 1.5 Google Material Design 3

**Material 3 Expressive (2025)** — анонсирована в мае 2025 для Android 16 и Wear OS 6:
- Увеличенная анимация
- Более красочный и современный дизайн
- Постепенный rollout на Pixel phones (Pixel 6+)

**Компонентная библиотека**:
- 30+ UI-компонентов с детальными спецификациями
- Богатая документация: usage, behavior, specification для каждого паттерна
- Поддержка быстрого onboarding

**Framework Implementations**:
- **Flutter**: Material 3 — дефолтный design language с Flutter 3.16
- **Angular**: Angular Material для mobile/desktop веб-приложений

**Foundations**:
- Accessibility standards
- Layout и interaction паттерны
- Design kits для Figma, Adobe, Sketch

**Источник**: [Material Design 3](https://m3.material.io/), [Components](https://m3.material.io/components), [Foundations](https://m3.material.io/foundations)

---

## 2. Design Tokens: W3C Specification 2025

### 2.1 W3C Design Tokens Specification 2025.10

**Первая стабильная версия** (релиз 28 октября 2025):
- Production-ready, vendor-neutral формат
- 20+ редакторов и авторов из Adobe, Amazon, Google, Meta, Figma, Shopify, Sketch и др.

**Ключевые возможности**:
- **Modern color spaces**: Display P3, Oklch, все CSS Color Module 4 spaces
- **Token relationships**: наследование, aliases, component-level references
- **Cross-platform consistency**: один token-файл → генерация для iOS, Android, Web, Flutter
- **Composite types**: shadows, gradients, borders, typography (multi-value structures)

**Источник**: [W3C Design Tokens](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)

---

### 2.2 Token Hierarchy & Best Practices

**Уровни токенов**:
1. **Foundation tokens** — core values (никогда не меняются):
   - Typography, Spacing, Radius, Foundation Colors
2. **Alias tokens** — адаптация для тем (Light/Dark/High Contrast)
3. **Component-specific tokens** — компонентные значения

**Naming Conventions**:
- **Иерархическая структура**: `color.primary.background`, `typography.heading.large`
- **Semantic naming**: описывать purpose, не appearance
  - ✅ `button-primary-background`
  - ❌ `blue-button`

**Typography Tokens**:
- Font-family, font-size, line-height, font-weight, letter-spacing, text-case, text-decoration
- Примеры: `font-heading-lg`, `font-body-sm`

**Spacing Tokens**:
- Консистентные единицы: `spacing-xs` (4px), `spacing-md` (16px)
- Базируются на vertical rhythm для читаемости

**Источник**: [USWDS Design Tokens](https://designsystem.digital.gov/design-tokens/), [Naming Conventions](https://medium.com/@wicar/streamlining-your-design-system-a-guide-to-tokens-and-naming-conventions-3e4553aa8821)

---

## 3. UX Specification Standards

### 3.1 WCAG 2.2 — Accessibility Baseline 2025

**Статус**: ISO/IEC 40500:2025, W3C Recommendation (конец 2023), baseline compliance 2025.

**Новое в WCAG 2.2**:
- 9 новых success criteria
- WCAG 3.0 на горизонте (но 2.2 — текущий стандарт)

**4 принципа WCAG**:
1. **Perceivable** — информация должна восприниматься
2. **Operable** — UI должен быть управляемым
3. **Understandable** — информация и UI должны быть понятными
4. **Robust** — контент должен корректно интерпретироваться assistive technologies

**Уровни соответствия**:
- **A** — минимум
- **AA** — рекомендуемый (баланс accessibility + практичность)
- **AAA** — высший

**Источник**: [WCAG 2025 Guidelines](https://www.wcag.com/resource/ux-quick-tips-for-designers/), [W3C WCAG Overview](https://www.w3.org/WAI/standards-guidelines/wcag/)

---

### 3.2 European Accessibility Act (EAA)

**Ключевые дедлайны 2025**:
- **28 июня 2025** — все новые продукты/сервисы должны полностью соответствовать EAA
- EAA выравнивается с **WCAG 2.1 AA** как технический бенчмарк
- Требования: text alternatives для изображений, достаточный цветовой контраст, keyboard-friendly навигация

**Источник**: [2025 Accessibility Regulations](https://medium.com/design-bootcamp/2025-accessibility-regulations-for-designers-how-wcag-eaa-and-ada-impact-ux-ui-eb785daf4436)

---

### 3.3 User Journey Mapping & Accessibility

**Inclusive Journey Mapping**:
- Не проектировать для одного "типичного" пользователя
- Карта взаимодействия для разных способностей и методов взаимодействия

**Diverse Participants**:
- Люди, использующие screen readers и assistive technologies
- Эксклюзивная клавиатурная навигация
- Разные уровни tech familiarity
- Color blindness или low vision
- Нужда в дополнительном времени для обработки информации
- Использование magnification tools

**Документирование на каждом этапе**:
- Potential accessibility barriers
- Alternative interaction paths
- Required assistive technology support
- Области, где пользователям нужна дополнительная помощь
- Точки с высокой cognitive load

**Источник**: [Accessible User Journey Maps](https://fastercapital.com/content/Ensuring-Accessibility-in-User-Journey-Maps.html)

---

## 4. Component Specifications

### 4.1 Component State Documentation

**6 обязательных состояний** для каждого интерактивного компонента:

1. **Default** — начальное состояние, элемент доступен для взаимодействия
2. **Focused** — focus indicator (focus ring) для текущего элемента
   - **Accessibility requirement**: каждый интерактивный элемент ДОЛЖЕН иметь focused state
3. **Hover** — реакция при наведении курсора (декоративное, signifies availability)
4. **Pressed/Active** — активное состояние при нажатии
5. **Disabled** — компонент недоступен, курсор показывает unavailability
6. **Invalid** — некорректный контент (особенно в формах)
7. **Loading** — загрузка или получение данных

**Дополнительные состояния**:
- **Selected** — выбранный элемент
- **Error** — ошибка валидации
- **Success** — успешная операция

**Важно**: Состояния могут сосуществовать (например, selected + hovered).

**Accessibility для состояний**:
- WCAG 2.0 SC 1.4.1: состояния не должны указываться только цветом
- Пример: изменение border color с gray на red + текст ошибки (не только цвет)

**Источник**: [Component States](https://jansensan.net/blog/ensure-design-all-states-every-interactive-component), [Interaction States](https://ariane.maze.co/latest/foundations/design/interaction-states-Fge8dLpi)

---

### 4.2 Component Specification Template

**Обязательные секции**:

1. **Purpose & Usage**:
   - Когда использовать компонент
   - Когда НЕ использовать
   - Use cases и примеры

2. **Anatomy**:
   - Структура компонента
   - Именование частей
   - Обязательные vs опциональные элементы

3. **States**:
   - Все 6+ состояний с визуальными спецификациями
   - Переходы между состояниями
   - Триггеры состояний

4. **Behavior**:
   - Взаимодействие с пользователем
   - Transitions и animations
   - Responsive behavior

5. **Accessibility**:
   - Keyboard navigation
   - Focus management
   - Screen reader support
   - ARIA attributes
   - Color contrast requirements

6. **Variants**:
   - Размеры (S, M, L)
   - Типы (primary, secondary, tertiary)
   - Themes (light, dark)

7. **Spacing & Layout**:
   - Padding, margins
   - Min/max sizes
   - Grid alignment

8. **Code Specifications**:
   - HTML structure
   - CSS classes
   - Props/parameters
   - Dependencies

**Источник**: [Component Specs](https://medium.com/eightshapes-llc/component-specifications-1492ca4c94c), [Salesforce Design Spec](https://trailhead.salesforce.com/content/learn/modules/systems-design-with-slds/document-design-guidelines-and-specifications)

---

## 5. Motion Design Specifications

### 5.1 Motion Principles & Styles

**Carbon Design System** — 2 стиля motion:

1. **Productive Motion** (быстрая, утилитарная):
   - Для task-focused моментов
   - Microinteractions: button states, dropdowns, data tables
   - Короткая duration

2. **Expressive Motion** (выразительная, заметная):
   - Для значимых моментов
   - Открытие страницы, primary action button, system alerts
   - Более длинная duration, энергичная

**Источник**: [Carbon Motion](https://carbondesignsystem.com/elements/motion/overview/)

---

### 5.2 Duration & Easing Guidelines

**Duration**:
- Динамическая, зависит от размера анимации
- Больше изменение distance/size → длиннее анимация
- Баланс между sluggish и abrupt

**Easing**:
- **Best practice**: Создать custom curves, не использовать CSS defaults
- Минимум 3 кривые: custom ease-out, ease-in, ease-in-out
- Консистентная motion association для бренда

**Microsoft Fluent 2**: Duration и easing гарантируют, что люди успевают заметить motion и интерпретировать его смысл.

**Источник**: [Fluent 2 Motion](https://fluent2.microsoft.design/motion)

---

### 5.3 Motion Tokens & Classes

**Atomic Design для Motion**:
- Каждая сложная анимация построена из organisms → molecules → atoms
- Developers создают "classes" для каждого элемента
- Переиспользование при создании новых анимаций
- Консистентность + легкость system-wide modifications

**Motion Tokens**:
- Токены для duration, easing, delay
- Применение как для color/spacing tokens
- Примеры: `duration-short`, `easing-standard`, `delay-enter`

**Transition Patterns**:
- Pre-defined способы переходов между состояниями
- Консистентное motion behavior по всему продукту
- Alignment с motion principles

**Источник**: [Motion Design System Guide](https://medium.com/@aviadtend/motion-design-system-practical-guide-8c15599262fe), [GitLab Animation Fundamentals](https://design.gitlab.com/product-foundations/animation-fundamentals/)

---

### 5.4 Motion Purposes (GitLab Pajamas)

1. **Feedback** — подтверждение взаимодействия
2. **Focus** — выделение важного контента вне текущего контекста
3. **Explanation** — показ свойств и отношений элементов
4. **Engagement** — поддержка пользователя во время ожидания
5. **Emotional** — эмоциональная связь, выражение бренда

**Accessibility**: Animation должна быть optional, использовать `prefers-reduced-motion` CSS media query.

**Источник**: [GitLab Animation](https://design.gitlab.com/product-foundations/animation-fundamentals/)

---

## 6. Responsive Design Specifications

### 6.1 Breakpoints 2025

**Рекомендуемые breakpoints**:
- **320px** — Small mobile
- **480px** — Large mobile (поддержка 375-430px современных смартфонов)
- **768px** — Tablets (portrait)
- **1024px** — Small desktop / Tablets (landscape)
- **1200px** — Standard desktop
- **1440px+** — Large desktop

**Статистика (North America)**:
- 375×812 (iPhone) — 16.79%
- 390×844 (Android) — 13.72%

**Источник**: [BrowserStack Breakpoints](https://www.browserstack.com/guide/responsive-design-breakpoints), [Responsive Design 2025 Playbook](https://dev.to/gerryleonugroho/responsive-design-breakpoints-2025-playbook-53ih)

---

### 6.2 Mobile-First Approach

**Индустриальный стандарт 2025**:
- 70%+ веб-трафика с мобильных устройств
- Mobile-first критичен для retention и SEO

**Mobile-First Media Queries**:
- Использование `min-width` queries
- Layering enhancements поверх мобильной базы
- Меньшие initial payloads, лучшая производительность

**Tailwind CSS**:
- Mobile-first breakpoint system
- Unprefixed utilities (например, `uppercase`) работают на всех размерах
- Prefixed utilities (например, `md:uppercase`) активируются с breakpoint и выше

**Источник**: [Tailwind Responsive Design](https://tailwindcss.com/docs/responsive-design), [Mobile-First Best Practices](https://nextnative.dev/blog/responsive-design-best-practices)

---

### 6.3 Content-Driven vs Device-Driven Breakpoints

**Best Practice**:
- Content-driven breakpoints часто превосходят device-driven
- Внедрять изменения там, где design естественно ломается
- Не привязываться к стандартным device dimensions

**Segment Breakpoints**:
- **Global breakpoints** — для page structure changes
- **Local (component-scoped) breakpoints** — для responsive components

**Источник**: [Content-Driven Breakpoints](https://www.causelabs.com/post/digital-breakpoints-responsive-design/)

---

## 7. Iconography Guidelines

### 7.1 Size & Grid Specifications

**Рекомендуемые размеры**:
- **24×24px** или **32×32px** для базового дизайна (divisible by 8 для 8pt grid)
- **Atlassian**: 16×16px bounding box, Medium icons (default)
- **IBM**: 32×32px grid, линейное масштабирование вниз

**Источник**: [Iconography Guide](https://www.designsystems.com/iconography-guide/), [Atlassian Iconography](https://atlassian.design/foundations/iconography/), [IBM UI Icons](https://www.ibm.com/design/language/iconography/ui-icons/design/)

---

### 7.2 Color & Consistency Guidelines

**Color**:
- Для product icons: **1 color (черный)**
- Больше цветов → компоненты становятся сложными и трудными для переиспользования
- Использование icon-specific color tokens или text color tokens
- Design tokens обеспечивают достаточный color contrast

**Consistency**:
- Один иконка = одна концепция/действие
- Не использовать разные иконки для одного значения
- Избегать использования одной иконки для несвязанных концепций

**Источник**: [GitLab Iconography](https://design.gitlab.com/product-foundations/iconography/)

---

### 7.3 Design Principles

**Balance Simplicity & Detail**:
- Простота для быстрого распознавания
- Достаточная детализация для передачи смысла даже в малых размерах

**Metaphors**:
- Positive или neutral metaphors
- Избегать концепций насилия или негативных ассоциаций

**Shape**:
- Четкость, минимализм, геометрия
- Улучшение читаемости на малых и больших размерах
- Использование узнаваемых метафор

**Cohesive System**:
- Консистентные размер, форма, стиль по всему set
- Accessibility: color values в dark, medium, light ranges
- Минимум половина иконки должна проходить 3.0:1 contrast ratio на light/dark темах

**Источник**: [UXcel Iconography](https://uxcel.com/blog/beginners-guide-to-iconography), [Iconography Guidelines](https://procreator.design/blog/iconography-guidelines/)

---

### 7.4 Maintenance & Organization

**Subcategories**:
- Разделение иконок на подкатегории по размеру и стилю
- Например: regular icons, detailed icons, illustrations
- Нет универсального правила — зависит от design system и количества иконок

**Источник**: [Iconography in Design Systems](https://www.smashingmagazine.com/2024/04/iconography-design-systems-troubleshooting-maintenance/)

---

## 8. Developer Handoff Excellence

### 8.1 Figma Dev Mode (2025)

**Dev Mode** — фундаментальный сдвиг в designer-developer collaboration:
- Structured access к specs, assets, documentation
- Более гладкий, быстрый, безошибочный handoff

**Ключевые возможности**:
- Сравнение frames с предыдущими версиями (что изменилось)
- Section statuses для обозначения ready-for-dev screens
- Автоматическая экстракция specs (spacing, typography, colors)

**Источник**: [Figma Developer Handoff](https://www.figma.com/best-practices/guide-to-developer-handoff/), [Figma Dev Mode Guide](https://designilo.com/2025/07/10/the-ultimate-figma-dev-mode-guide-with-handoff-checklists/)

---

### 8.2 Documentation Best Practices

**Two-Place Documentation**:
- **Inline в Figma** — руководство внутри дизайн-системы
- **CSS Strategy Guide** — comprehensive для developers

**Преимущества inline**:
- Designers и developers используют один source of truth
- Guidance видна exactly when needed
- Не устаревает (как separate documents)

**Что включать**:
- Component purpose (когда использовать, когда не использовать)
- Flexibility guidelines (что можно модифицировать, что нет)
- Usage examples
- Interaction patterns
- Accessibility notes
- Architecture decisions
- Extending patterns
- File organization
- Best practices
- Quick reference (essential classes, variables, patterns)

**Источник**: [Design System Handoff Documentation](https://thoughtbot.com/blog/leaving-clients-with-more-than-a-figma-file-a-guide-to-design-system-handoff-documentation)

---

### 8.3 File Organization

**Структура**:
- Организация по feature/flow, не только по screens
- Архивы и iterations отдельно от production-ready designs
- Четкие naming conventions
- Маркировка frames "Ready for Dev"

**Коммуникация**:
- Developers получают доступ к файлам с десятками in-progress frames
- Важно коммуницировать, какие части ready for implementation, а какие in progress

**Источник**: [Figma Tips on Developer Handoff](https://www.figma.com/best-practices/tips-on-developer-handoff/)

---

### 8.4 Common Handoff Mistakes

**Избегать**:
- ❌ Использование local colors/fonts вместо styles
- ❌ Messy layers без naming structure
- ❌ Отсутствие export settings для изображений
- ❌ Inconsistent spacing или misaligned grids
- ❌ Отсутствие документации для interaction states или edge cases

**Best Practices**:
- ✅ Использование variables, tokens, shared styles
- ✅ Запуск plugins (Design System Tracker) для проверки rogue/detached styles
- ✅ Согласование naming conventions для Styles в начале проекта
- ✅ Проверка color contrast, focus states, tab order
- ✅ Тестирование с screen readers и keyboard navigation

**Источник**: [The Designer's Handbook for Developer Handoff](https://www.figma.com/blog/the-designers-handbook-for-developer-handoff/), [Eleken Handoff Guide](https://www.eleken.co/blog-posts/figma-developer-handoff-collaborate-like-eleken-designers)

---

### 8.5 Useful Plugins

- **Zero Height** — синхронизация Figma компонентов/styles, автоматизация создания design systems и документации
- **Design System Tracker** — проверка rogue или detached styles перед handoff

**Источник**: [Smashing Magazine Handoff File](https://www.smashingmagazine.com/2023/05/designing-better-design-handoff-file-figma/)

---

## 9. Storybook Integration

### 9.1 Storybook для Design Systems (2025)

**Storybook** — frontend workshop для построения UI-компонентов в изоляции:
- Automatic documentation из компонентов
- UI, examples, documentation в одном месте
- Тысячи команд используют для UI development, testing, documentation

**Источник**: [Storybook](https://storybook.js.org/)

---

### 9.2 Supernova Integration (May 2025)

**Supercharged Storybook Integration**:
- Контроль видимости properties (показывать только relevant)
- Кастомизация column display
- Управление tabs (только нужные секции)
- Редактирование properties в editor (изменения сохраняются в published docs)

**Private Hosting**:
- Для Storybooks за VPN или authentication
- Deploy через CLI напрямую в Supernova
- Private, secure hosting с seamless access

**Источник**: [Supernova Storybook Integration](https://learn.supernova.io/latest/releases/may-2025/new-storybook-integration-and-hosting-IhMWfZsP)

---

### 9.3 Design Tool Integrations

**Figma**:
- Storybook Connect plugin — embed component stories в Figma
- Powered by Storybook embeds и Chromatic

**Zeroheight**:
- Collaborative styleguide generator
- Design, code, brand, copywriting в одном месте
- WYSIWYG editor для документации
- Embed stories рядом с design specs

**UXPin**:
- Interactive design tool с production code
- Использование interactive stories для design user flows

**Zeplin**:
- Zeplin addon для Storybook
- Дизайны из Zeplin рядом с currently selected story
- Tooling для overlay design image поверх live component

**Источник**: [Storybook Design Integrations](https://storybook.js.org/docs/sharing/design-integrations)

---

### 9.4 Benefits & Considerations

**Benefits**:
- Bridging gap между design и development
- Улучшенная collaboration, testing edge cases
- Single source of truth между командами
- Команды экономят до 10 часов/неделю через improved collaboration

**Considerations**:
- Component-centric подход — отсутствие narrative structure
- Сложность для non-technical team members понять overarching design principles
- Documentation может казаться fragmented и disconnected

**Источник**: [Storybook for Designers](https://www.supernova.io/blog/storybook-for-designers-why-its-more-than-just-a-dev-tool), [Should you document in Storybook?](https://zeroheight.com/help/guides/should-you-document-your-design-system-in-storybook/)

---

## 10. Design QA & Visual Regression Testing

### 10.1 Visual Regression Testing

**Определение**:
- QA practice для верификации visual interface
- Сравнение screenshots UI до и после изменений
- Обнаружение unintended discrepancies
- Гарантия UI integrity в rapid development cycles

**Цель**:
- Верификация, что application's front end рендерится exactly as designed
- Safety net для UI integrity
- Обеспечение intentional changes

**Источник**: [Visual Regression Testing 2025](https://www.getpanto.ai/blog/visual-regression-testing-in-mobile-qa)

---

### 10.2 Visual Regression Tools (2025)

**Panto AI** — premier choice для mobile QA 2025:
- AI-powered platform
- Codeless & AI-driven test generation
- Self-healing capabilities (адаптация к minor UI changes)
- Mobile-first deep integration (Appium, Maestro)

**Applitools**:
- Market veteran, powerhouse в visual debugging
- Visual AI для игнорирования false positives

**LambdaTest SmartUI**:
- Intelligent visual regression в cloud
- Сравнение layouts, text, graphics по wide range mobile browsers
- Easy setup для Selenium/Cypress teams

**Источник**: [Visual Regression Tools](https://www.getpanto.ai/blog/visual-regression-testing-in-mobile-qa)

---

### 10.3 Design QA Checklist

**Key Elements**:

1. **Visual Balance**:
   - Alignment элементов (margins, paddings, borders)
   - Единый focal point в grid
   - Позиционирование относительно grid

2. **Text Contrast**:
   - WCAG 1.4.3 contrast minimum
   - 5% людей с color blindness
   - Google рекомендует исправлять low-contrast issues

3. **Consistency**:
   - Все компоненты одного типа с одинаковыми hover/active states
   - Unified experience

4. **Feedback**:
   - Четкая и немедленная обратная связь на user actions

**Источник**: [Design QA Checklist](https://www.eleken.co/blog-posts/design-qa-checklist-to-test-ui-and-prepare-for-design-handoff)

---

### 10.4 QA Testing Best Practices

**Testing Plan**:
- Четкие quality standards
- Testing objectives и methods
- Множественные QA tests:
  - Functional testing
  - Usability testing
  - Cross-browser/cross-device testing
  - Regression testing
  - Load testing
  - Accessibility testing

**Shift Left Testing**:
- QA involvement с ранних стадий (requirement gathering, design)
- Идентификация issues до costly problems

**Automated Testing**:
- Scripts и tools (Selenium, Cypress)
- Идеален для regression, performance, repetitive tasks

**Источник**: [Website QA Testing 2025](https://bugherd.com/blog/website-qa-testing-complete-guide-to-quality-assurance-in-2025), [QA Best Practices](https://www.browserstack.com/guide/qa-best-practices)

---

## 11. Design System Audit & Checklist

### 11.1 Design System Audit

**Определение**:
- Evaluation существующих UI components, pattern libraries, design policies
- Идентификация областей для improvement
- Первый шаг в revamping существующей design system

**Цель**:
- Comprehensive evaluation продукта: UI, functionality, overall design
- Magnifying glass для brand's visual elements
- Обеспечение консистентности brand image, vibe, messaging

**Источник**: [Ramotion Design System Audit](https://www.ramotion.com/blog/design-system-audit/), [The Design System Guide](https://thedesignsystem.guide/design-audit)

---

### 11.2 Audit Resources & Templates

**Figma Templates**:
- [Design System Checklist 2025](https://www.figma.com/community/file/1479810788762292490/design-system-checklist-2025) — comprehensive template, structured framework
- [Design Audit Template](https://www.figma.com/community/file/1225028471286293075/design-audit-template) — all-in-one solution

**Open-Source Checklists**:
- [Design System Checklist](https://www.designsystemchecklist.com/) — plan, build, grow your design system

**Platform-Specific**:
- [Webflow Design System Checklist](https://university.webflow.com/resources/design-system-checklist) — documentation, roles, regular audits, accessibility expectations

**Design Token Audit**:
- [Meegle Design Token Audit Checklist](https://www.meegle.com/en_us/advanced-templates/user_interface/design_token_audit_checklist_template) — audit colors, typography, spacing, consistency

**Источник**: См. ссылки выше

---

### 11.3 Accessibility in Audits

**Accessibility Focus**:
- Нельзя пренебрегать accessibility — essential в design system audit
- Detailed checklist для каждого компонента
- Accessibility tools и W3C preliminary tests
- Inspiration от IBM, Google design systems

**Webflow Recommendations**:
- Использовать Accessibility checklist и Audit panel
- Документировать accessibility expectations рядом с visual/structural rules
- Тестирование с assistive technologies:
  - Screen readers
  - Browser zoom и font-size settings
  - Keyboard-only navigation

**Источник**: [Aufait UX Audit](https://www.aufaitux.com/blog/ui-ux-design-system-audit/), [Webflow Checklist](https://university.webflow.com/resources/design-system-checklist)

---

## Frameworks & Checklists для /speckit.design

### Framework 1: Design System Maturity Model

**5 уровней зрелости**:

**Level 1 — Ad Hoc**:
- Нет design system
- Designers создают UI на основе индивидуальных решений
- Inconsistency между проектами

**Level 2 — Style Guide**:
- Базовый style guide (цвета, типографика)
- Static documentation
- Minimal component library

**Level 3 — Component Library**:
- Reusable components
- Basic governance model
- Version control для компонентов

**Level 4 — Design System**:
- Comprehensive design tokens
- Cross-platform support
- Automated testing
- Clear contribution process
- Accessibility built-in

**Level 5 — Ecosystem**:
- Multiple products использующие единую систему
- Advanced tooling (Storybook, Figma sync)
- Community contributions
- Continuous evolution
- Metrics-driven optimization

---

### Framework 2: Design Specification Completeness Score (DSCS)

**10 категорий по 10 баллов каждая (max 100)**:

1. **Design Tokens** (10 points):
   - Color tokens (light/dark themes)
   - Typography tokens
   - Spacing tokens
   - Shadow/elevation tokens
   - Border radius tokens

2. **Component States** (10 points):
   - Default, Focused, Hover, Pressed, Disabled, Invalid, Loading
   - State transitions documented

3. **Accessibility** (10 points):
   - WCAG 2.2 AA compliance
   - Keyboard navigation specs
   - Screen reader support
   - Color contrast verification
   - Focus management

4. **Responsive Behavior** (10 points):
   - Breakpoint specifications
   - Mobile-first approach
   - Content-driven breakpoints
   - Component-level responsive rules

5. **Motion Design** (10 points):
   - Duration specifications
   - Easing curves
   - Motion tokens
   - Transition patterns
   - Accessibility (prefers-reduced-motion)

6. **Iconography** (10 points):
   - Size & grid specs
   - Color guidelines
   - Consistency rules
   - Metaphor guidelines

7. **Developer Handoff** (10 points):
   - Figma Dev Mode usage
   - Export settings
   - Naming conventions
   - Code snippets
   - Edge cases documented

8. **Documentation Quality** (10 points):
   - Inline + external docs
   - Usage examples
   - Do's and don'ts
   - Variants documented
   - Storybook integration

9. **Visual Regression** (10 points):
   - Automated visual testing
   - Screenshot comparisons
   - Cross-browser testing
   - QA checklist

10. **Governance** (10 points):
    - Ownership model
    - Contribution process
    - Versioning strategy
    - Review process

**Grading**:
- 90-100: World-class
- 75-89: Enterprise-ready
- 60-74: Solid foundation
- 40-59: Needs improvement
- 0-39: Ad hoc

---

### Framework 3: Component Specification Template

```markdown
# [Component Name]

## Purpose
**When to use**: [Scenarios]
**When NOT to use**: [Anti-patterns]

## Anatomy
[Visual breakdown с именованием частей]
- **Required elements**: [List]
- **Optional elements**: [List]

## States
| State | Visual | Trigger | Accessibility |
|-------|--------|---------|---------------|
| Default | [Spec] | Initial load | [ARIA] |
| Focused | [Spec] | Keyboard tab | Focus ring required |
| Hover | [Spec] | Mouse over | [ARIA] |
| Pressed | [Spec] | Click/tap | [ARIA] |
| Disabled | [Spec] | Prop disabled | aria-disabled="true" |
| Invalid | [Spec] | Validation fail | aria-invalid="true" |
| Loading | [Spec] | Data fetch | aria-busy="true" |

## Variants
| Variant | Use Case | Visual |
|---------|----------|--------|
| Primary | Main action | [Spec] |
| Secondary | Alternative action | [Spec] |
| Tertiary | Subtle action | [Spec] |

## Sizes
| Size | Height | Padding | Font Size | Use Case |
|------|--------|---------|-----------|----------|
| Small | 32px | 12px | 14px | Dense UI |
| Medium | 40px | 16px | 16px | Default |
| Large | 48px | 20px | 18px | Touch targets |

## Spacing & Layout
- **Padding**: [Token reference]
- **Margin**: [Token reference]
- **Min width**: [Value]
- **Max width**: [Value]
- **Grid alignment**: [Rules]

## Motion
- **Transition**: [Duration] [Easing] [Properties]
- **Entrance**: [Animation spec]
- **Exit**: [Animation spec]

## Responsive Behavior
| Breakpoint | Behavior |
|------------|----------|
| <480px | [Mobile spec] |
| 480-768px | [Tablet spec] |
| >768px | [Desktop spec] |

## Accessibility
- **Keyboard navigation**: [Tab order, shortcuts]
- **Screen reader**: [ARIA labels, roles, live regions]
- **Focus management**: [Focus trapping, restoration]
- **Color contrast**: [Ratios for all states]

## Code Specifications
### HTML Structure
```html
[Example]
```

### CSS Classes
- `.component-name` - Base class
- `.component-name--variant` - Variant modifier
- `.component-name--size` - Size modifier

### Props/Parameters
| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| variant | string | 'primary' | No | Visual variant |
| size | string | 'medium' | No | Size variant |
| disabled | boolean | false | No | Disabled state |

### Dependencies
- [Design token dependencies]
- [Component dependencies]

## Usage Examples
### Basic Usage
[Code example]

### Advanced Usage
[Code example with edge cases]

## Do's and Don'ts
✅ **Do**: [Best practices]
❌ **Don't**: [Anti-patterns]

## Related Components
- [Links to related components]

## Version History
- v1.0.0 (2025-01-03): Initial release
```

---

### Checklist 1: Design System Foundation Audit

**Design Tokens** (Foundation):
- [ ] Color palette defined (primary, secondary, neutral, semantic)
- [ ] Light/dark theme tokens specified
- [ ] Typography scale established (font families, sizes, weights, line heights)
- [ ] Spacing scale defined (4px/8px base, consistent rhythm)
- [ ] Shadow/elevation tokens documented
- [ ] Border radius tokens specified
- [ ] Transition/animation tokens established
- [ ] W3C Design Tokens Specification 2025.10 format used
- [ ] Token naming follows semantic conventions (not presentational)
- [ ] Cross-platform token export (iOS, Android, Web)

**Component Library**:
- [ ] Core components identified and prioritized
- [ ] Component anatomy documented for each component
- [ ] All 6+ interaction states specified (default, focused, hover, pressed, disabled, invalid, loading)
- [ ] State transitions defined
- [ ] Component variants documented (sizes, types, themes)
- [ ] Responsive behavior specified
- [ ] Motion specifications included
- [ ] Code implementation examples provided
- [ ] Storybook integration configured

**Governance**:
- [ ] Component ownership model established
- [ ] Contribution process documented
- [ ] Versioning strategy defined (semantic versioning)
- [ ] Review/approval process specified
- [ ] Cross-functional working groups identified
- [ ] Release process documented

---

### Checklist 2: Accessibility Compliance (WCAG 2.2)

**Perceivable**:
- [ ] Text alternatives для non-text content
- [ ] Color contrast meets WCAG 2.2 AA (4.5:1 normal text, 3:1 large text)
- [ ] Color не единственный способ передачи информации
- [ ] Text resizable до 200% без потери функциональности
- [ ] Images of text используются минимально

**Operable**:
- [ ] Вся функциональность доступна с клавиатуры
- [ ] Keyboard trap отсутствует
- [ ] Timing adjustable для time limits
- [ ] No content flashing более 3 раз в секунду
- [ ] Skip navigation links provided
- [ ] Focus visible для всех интерактивных элементов
- [ ] Touch targets минимум 44×44px

**Understandable**:
- [ ] Language of page specified (lang attribute)
- [ ] Consistent navigation между страницами
- [ ] Consistent identification компонентов
- [ ] Error messages clear и actionable
- [ ] Labels и instructions для form inputs
- [ ] Error prevention для critical actions

**Robust**:
- [ ] Valid HTML markup
- [ ] ARIA attributes корректно использованы
- [ ] Name, role, value для UI components
- [ ] Assistive technology compatibility tested
- [ ] Status messages используют aria-live regions

**Testing**:
- [ ] Keyboard-only navigation tested
- [ ] Screen reader testing completed (NVDA, JAWS, VoiceOver)
- [ ] Color contrast verified (automated tools + manual)
- [ ] Zoom/magnification tested (200%, 400%)
- [ ] prefers-reduced-motion respected

---

### Checklist 3: Component Specification Completeness

**For each component**:

**Purpose & Usage**:
- [ ] When to use documented
- [ ] When NOT to use documented
- [ ] Use cases provided
- [ ] Best practices listed

**Anatomy**:
- [ ] Visual breakdown provided
- [ ] Parts named
- [ ] Required elements specified
- [ ] Optional elements specified

**States**:
- [ ] Default state specified
- [ ] Focused state specified (with focus ring)
- [ ] Hover state specified
- [ ] Pressed/Active state specified
- [ ] Disabled state specified
- [ ] Invalid state specified (if applicable)
- [ ] Loading state specified (if applicable)
- [ ] Selected state specified (if applicable)
- [ ] State transitions documented
- [ ] Triggers for each state documented

**Variants**:
- [ ] All variants identified (primary, secondary, tertiary, etc.)
- [ ] Visual specs for each variant
- [ ] Use cases for each variant

**Sizes**:
- [ ] Small size specified (if applicable)
- [ ] Medium size specified (default)
- [ ] Large size specified (if applicable)
- [ ] Dimensions (height, width, padding) documented

**Spacing & Layout**:
- [ ] Internal padding specified (token reference)
- [ ] External margins specified (token reference)
- [ ] Min/max dimensions specified
- [ ] Grid alignment rules documented

**Motion**:
- [ ] Transition duration specified
- [ ] Easing curve specified
- [ ] Animated properties listed
- [ ] Entrance animation documented
- [ ] Exit animation documented
- [ ] prefers-reduced-motion alternative provided

**Responsive Behavior**:
- [ ] Mobile (<480px) behavior specified
- [ ] Tablet (480-768px) behavior specified
- [ ] Desktop (>768px) behavior specified
- [ ] Component-specific breakpoints identified

**Accessibility**:
- [ ] Keyboard navigation documented (tab order, shortcuts)
- [ ] Screen reader support specified (ARIA labels, roles)
- [ ] Focus management documented
- [ ] Color contrast verified for all states
- [ ] Touch target size verified (44×44px min)

**Code**:
- [ ] HTML structure example provided
- [ ] CSS classes documented
- [ ] Props/parameters specified
- [ ] Dependencies listed
- [ ] Usage examples provided

**Documentation**:
- [ ] Do's listed
- [ ] Don'ts listed
- [ ] Related components linked
- [ ] Version history maintained

---

### Checklist 4: Developer Handoff Readiness

**Figma File Preparation**:
- [ ] Production-ready designs separated from iterations/archives
- [ ] Frames marked "Ready for Dev"
- [ ] Naming conventions applied consistently
- [ ] Layers organized и named (no "Frame 1", "Rectangle 23")
- [ ] Components используются (not local instances)
- [ ] Styles применены (colors, typography, effects)
- [ ] Auto-layout использован для responsive components
- [ ] Export settings configured для assets
- [ ] Dev Mode enabled и configured

**Design Tokens**:
- [ ] Variables created для colors, spacing, typography
- [ ] Token naming semantic (не presentational)
- [ ] Token collections organized (primitives, semantic, component)
- [ ] Light/dark theme tokens separated
- [ ] Tokens exported в W3C format

**Documentation**:
- [ ] Inline comments для complex interactions
- [ ] Component documentation embedded
- [ ] Accessibility notes included
- [ ] Responsive behavior documented
- [ ] Edge cases called out
- [ ] Interaction states annotated

**Assets**:
- [ ] Icons exported в required formats (SVG, PNG)
- [ ] Images optimized
- [ ] Asset naming convention followed
- [ ] Asset organization structure clear

**Specifications**:
- [ ] Spacing inspectable (Auto-layout or annotations)
- [ ] Typography styles inspectable
- [ ] Color styles inspectable
- [ ] Effects (shadows, blurs) inspectable
- [ ] Border radius inspectable

**Cross-Browser/Platform**:
- [ ] Design tested на multiple screen sizes
- [ ] Breakpoints clearly communicated
- [ ] Platform-specific considerations documented (iOS vs Android vs Web)

**QA Checks**:
- [ ] Visual balance verified (alignment, spacing)
- [ ] Color contrast checked (WCAG compliance)
- [ ] Consistency across components verified
- [ ] No detached styles (run Design System Tracker)
- [ ] No local colors/fonts (all using styles)

**Handoff Meeting**:
- [ ] Walkthrough scheduled
- [ ] Key decisions documented
- [ ] Questions answered
- [ ] Timeline aligned

---

### Checklist 5: Visual Regression Testing Setup

**Tool Selection**:
- [ ] Visual regression tool выбран (Panto AI, Applitools, LambdaTest SmartUI, Percy, Chromatic)
- [ ] Tool интегрирован в CI/CD pipeline
- [ ] Baseline screenshots captured

**Test Coverage**:
- [ ] All components covered
- [ ] All component states covered (default, hover, focused, disabled, etc.)
- [ ] All component variants covered (sizes, types, themes)
- [ ] Responsive breakpoints covered
- [ ] Light/dark themes covered

**Configuration**:
- [ ] Screenshot comparison threshold configured
- [ ] Browsers/devices для testing specified
- [ ] Self-healing configured (if applicable)
- [ ] False positive handling configured

**CI/CD Integration**:
- [ ] Tests run on каждый PR
- [ ] Test results reported в PR comments
- [ ] Failing tests block merge
- [ ] Baseline update process documented

**Review Process**:
- [ ] Visual diff review process established
- [ ] Approval workflow defined
- [ ] Baseline update authorization specified

**Monitoring**:
- [ ] Visual regression trends tracked
- [ ] False positive rate monitored
- [ ] Test execution time monitored

---

### Checklist 6: Motion Design Specifications

**Motion Principles**:
- [ ] Motion style defined (productive vs expressive)
- [ ] Use cases для каждого style specified
- [ ] Motion purposes identified (feedback, focus, explanation, engagement, emotional)

**Duration**:
- [ ] Duration scales established (short, medium, long)
- [ ] Size-based duration rules defined (larger elements = longer duration)
- [ ] Token values specified (e.g., duration-short: 100ms, duration-medium: 300ms)

**Easing**:
- [ ] Custom easing curves created (не CSS defaults)
- [ ] Minimum 3 curves: ease-out, ease-in, ease-in-out
- [ ] Token values specified (e.g., easing-standard, easing-emphasized)

**Transition Patterns**:
- [ ] Pre-defined transition patterns documented
- [ ] Pattern use cases specified
- [ ] Code examples provided

**Animation Specs**:
- [ ] Entrance animations specified
- [ ] Exit animations specified
- [ ] Loading animations specified
- [ ] State transition animations specified

**Accessibility**:
- [ ] prefers-reduced-motion query implemented
- [ ] Reduced motion alternatives provided
- [ ] Animation optional, не required для функциональности

**Implementation**:
- [ ] Motion tokens created
- [ ] Motion classes/utilities created (atomic design approach)
- [ ] Animation reusable и composable
- [ ] Documentation для developers

---

### Checklist 7: Iconography System

**Size & Grid**:
- [ ] Base size established (24×24px or 32×32px, divisible by 8)
- [ ] Grid system defined
- [ ] Scaling rules documented
- [ ] Size variants specified (16px, 24px, 32px, etc.)

**Design Principles**:
- [ ] Simplicity vs detail balance defined
- [ ] Metaphor guidelines established (positive/neutral, no violence)
- [ ] Shape guidelines (clarity, minimalism, geometry)
- [ ] Consistency rules documented

**Color**:
- [ ] Color palette для icons (обычно 1 color: black)
- [ ] Color tokens specified
- [ ] Contrast requirements (3.0:1 minimum)
- [ ] Light/dark theme considerations

**Organization**:
- [ ] Icon subcategories defined (regular, detailed, illustrations)
- [ ] Naming convention established
- [ ] Icon library organized
- [ ] Icon versioning strategy

**Usage Guidelines**:
- [ ] One icon = one concept rule documented
- [ ] Icon consistency guidelines
- [ ] Do's and don'ts
- [ ] Accessibility guidelines (alt text, aria-labels)

**Implementation**:
- [ ] Icon format specified (SVG preferred)
- [ ] Export settings configured
- [ ] Icon component created (if applicable)
- [ ] Icon font generated (if applicable)

---

### Checklist 8: Responsive Design Specifications

**Breakpoints**:
- [ ] Breakpoint values defined (320px, 480px, 768px, 1024px, 1200px, 1440px+)
- [ ] Breakpoint naming convention established
- [ ] Mobile-first approach confirmed
- [ ] Content-driven breakpoints identified (не только device-driven)

**Layout**:
- [ ] Grid system defined (columns, gutters, margins)
- [ ] Grid behavior per breakpoint specified
- [ ] Container max-widths defined
- [ ] Spacing scale responsive behavior documented

**Typography**:
- [ ] Font size scales per breakpoint
- [ ] Line height adjustments per breakpoint
- [ ] Letter spacing adjustments (if any)

**Components**:
- [ ] Component responsive behavior documented
- [ ] Component-specific breakpoints identified
- [ ] Stacking/wrapping rules defined
- [ ] Touch target adjustments для mobile (44×44px min)

**Images/Media**:
- [ ] Responsive image strategy (srcset, sizes)
- [ ] Image aspect ratios per breakpoint
- [ ] Video responsive behavior

**Testing**:
- [ ] Cross-device testing completed
- [ ] Orientation testing (portrait/landscape)
- [ ] Zoom testing (200%, 400%)

---

## Рекомендации для интеграции в /speckit.design

### 1. Design System Maturity Assessment

**Первый шаг** при запуске `/speckit.design`:
- Оценка текущего уровня зрелости (Level 1-5)
- Определение целевого уровня
- Roadmap для достижения целевого уровня

### 2. Design Specification Completeness Score (DSCS)

**Автоматический расчет** для каждого компонента:
- Checklist-based scoring (10 категорий × 10 баллов)
- Визуализация gaps
- Приоритизация missing elements

### 3. Модульная структура команды

**Разбить `/speckit.design` на sub-commands**:
- `/speckit.design.tokens` — Design tokens specification
- `/speckit.design.components` — Component specifications
- `/speckit.design.motion` — Motion design specs
- `/speckit.design.accessibility` — A11y audit и specs
- `/speckit.design.handoff` — Developer handoff package
- `/speckit.design.audit` — Design system audit

### 4. Template-Based Generation

**Использовать шаблоны** из исследования:
- Component Specification Template (см. Framework 3)
- Checklists 1-8 как built-in validation
- Автоматическая генерация секций на основе best practices

### 5. Integration Points

**Интеграция с другими /speckit commands**:
- `/speckit.specify` → Design requirements extraction
- `/speckit.plan` → Design implementation tasks
- `/speckit.implement` → Design token code generation
- `/speckit.analyze` → Design-code consistency validation

### 6. Quality Gates

**DSCS как quality gate**:
- Минимум 75/100 для production-ready components
- Automated warnings для missing specs
- Progressive enhancement (можно начать с базовых specs, постепенно улучшать)

### 7. Industry Benchmarks

**Встроенные benchmarks** из топ-компаний:
- Apple HIG standards
- Material Design 3 specs
- Airbnb DLS governance
- Uber Base tokens architecture
- Stripe accessibility standards

---

## Ключевые метрики успеха

**Design System Adoption**:
- % компонентов использующих design tokens
- % компонентов с complete specifications
- Developer handoff time reduction
- Design-code consistency score

**Accessibility**:
- WCAG 2.2 AA compliance rate
- Accessibility issues caught в design phase
- Screen reader compatibility score

**Efficiency**:
- Time to spec new component (target: <2 hours)
- Handoff rework rate (target: <10%)
- Visual regression false positive rate (target: <5%)

**Quality**:
- Design Specification Completeness Score (target: 75+)
- Component reusability rate
- Cross-platform consistency score

---

## Sources

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [Airbnb Design System](https://karrisaarinen.com/dls/)
- [Uber Base Design System](https://base.uber.com/)
- [Stripe UI Components](https://docs.stripe.com/stripe-apps/components)
- [Material Design 3](https://m3.material.io/)
- [W3C Design Tokens Specification](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [WCAG 2.2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Figma Developer Handoff Guide](https://www.figma.com/best-practices/guide-to-developer-handoff/)
- [Storybook Documentation](https://storybook.js.org/)
- [Design System Checklist](https://www.designsystemchecklist.com/)
- [Carbon Design System Motion](https://carbondesignsystem.com/elements/motion/overview/)
- [GitLab Pajamas Iconography](https://design.gitlab.com/product-foundations/iconography/)
- [BrowserStack Responsive Breakpoints](https://www.browserstack.com/guide/responsive-design-breakpoints)
- [Visual Regression Testing 2025](https://www.getpanto.ai/blog/visual-regression-testing-in-mobile-qa)
