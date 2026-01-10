# Gherkin UI Example

This example demonstrates how to write acceptance criteria in Gherkin format PLUS Visual YAML for UI features.

## User Story: Product Search

**As a** customer
**I want to** search for products
**So that** I can quickly find what I need

**Priority**: P1a
**Concept Reference**: EPIC-002.F01.S02

---

## Acceptance Criteria (Gherkin)

<!--
  IMPORTANT: Executable Gherkin format for BDD frameworks (Cucumber, Behave, SpecFlow).
  For UI features, scenarios focus on user interactions and visual feedback.
-->

```gherkin
Feature: Product Search

Search for products by keyword with real-time results, filters, and empty state handling.

Scenario: AS-2A - Search with results found [HAPPY_PATH] [Confidence: 0.95]
  Given database contains 15 products matching "laptop"
  And I am on the homepage
  When I enter "laptop" in "search input"
  And I click "Search" button
  Then search results appear within 500ms
  And results list shows 10 items
  And each result shows product image, title, price
  And pagination shows "Page 1 of 2"
  And sort dropdown is visible with default "Relevance"
  And filter panel shows categories and price ranges
  And URL updates to "/search?q=laptop"
  And page title is "Search results for 'laptop'"

Scenario: AS-2B - Search with no results [ALT_PATH] [Confidence: 0.90]
  Given database contains no products matching "nonexistent"
  And I am on the homepage
  When I enter "nonexistent" in "search input"
  And I click "Search" button
  Then empty state appears within 500ms
  And empty state shows message "No products found for 'nonexistent'"
  And empty state shows illustration
  And suggestions panel appears with text "Try these popular searches:"
  And suggestions show 5 trending search terms
  And results list is hidden
  And URL updates to "/search?q=nonexistent"

Scenario: AS-2C - Real-time search suggestions [ALT_PATH] [Confidence: 0.88]
  Given database contains products matching "lap"
  And I am on the homepage
  When I type "lap" in "search input"
  Then autocomplete dropdown appears within 300ms
  And autocomplete shows top 5 product matches
  And autocomplete shows top 3 category matches
  And each suggestion shows product name and price
  And matching text "lap" is highlighted in bold
  When I press "ArrowDown" key
  Then first suggestion is highlighted
  When I press "Enter" key
  Then highlighted product page opens

Scenario: AS-2D - Filter results by category [ALT_PATH] [Confidence: 0.85]
  Given I have search results for "laptop"
  And results show 15 products across 3 categories
  When I click "Electronics" checkbox in filter panel
  Then results refresh within 300ms
  And results show only products in "Electronics" category
  And result count updates to "8 products found"
  And filter pill "Electronics" appears above results
  And URL updates to "/search?q=laptop&category=electronics"
  When I click "X" on "Electronics" filter pill
  Then filter is removed
  And all 15 results appear again

Scenario: AS-2E - Sort results by price [ALT_PATH] [Confidence: 0.82]
  Given I have search results for "laptop"
  And results show 15 products
  When I select "Price: Low to High" from sort dropdown
  Then results refresh within 300ms
  And results are ordered by price ascending
  And first product price is less than second product price
  And URL updates to "/search?q=laptop&sort=price_asc"
  And sort dropdown shows "Price: Low to High" as selected

Scenario: AS-2F - Search with special characters (XSS prevention) [SECURITY] [Confidence: 0.90]
  Given I am on the homepage
  When I enter "<script>alert('XSS')</script>" in "search input"
  And I click "Search" button
  Then search executes safely without executing script
  And results page shows escaped query in breadcrumb
  And no JavaScript alert appears
  And XSS attempt is logged to security system
  And search query is sanitized in URL

Scenario: AS-2G - Pagination navigation [BOUNDARY] [Confidence: 0.80]
  Given I have search results for "laptop" with 25 products
  And I am on page 1 showing products 1-10
  When I click "Next" button
  Then page 2 loads within 400ms
  And products 11-20 are displayed
  And pagination shows "Page 2 of 3"
  And URL updates to "/search?q=laptop&page=2"
  And page scrolls to top
  And "Previous" button is now enabled
  When I click "Previous" button
  Then page 1 loads
  And products 1-10 are displayed

Scenario: AS-2H - Empty search query validation [BOUNDARY] [Confidence: 0.75]
  Given I am on the homepage
  And search input is empty
  When I click "Search" button
  Then search does not execute
  And error message appears below input: "Please enter a search term"
  And error message is red with icon
  And error message disappears after 3000ms
  And input border turns red
  And no navigation occurs

Scenario: AS-2I - Search loading state [ALT_PATH] [Confidence: 0.78]
  Given I am on the homepage
  When I enter "laptop" in "search input"
  And I click "Search" button
  Then immediately:
    - Search button shows spinner
    - Search button is disabled
    - Search input is disabled
    - Loading skeleton appears in results area
  And after 500ms:
    - Actual results replace skeleton
    - Search button returns to normal state
    - All inputs are re-enabled

Scenario: AS-2J - Mobile responsive search [BOUNDARY] [Confidence: 0.80]
  Given I am on the homepage
  And viewport width is 375px (mobile)
  When I click search icon in header
  Then search overlay appears covering entire screen
  And search input is focused automatically
  And search input width is 100% of screen minus padding
  And filter panel is collapsed with "Filters" button
  When I click "Filters" button
  Then filter panel slides up from bottom as modal
  And filter modal has "Apply" and "Cancel" buttons
```

---

## Visual Acceptance Criteria *(for UI features)*

<!--
  YAML format for UI state, layout, and responsive behavior.
  Complements executable Gherkin scenarios with visual specifications.
-->

```yaml
product_search_page:
  elements:
    - search_input:
        visible: true
        type: search
        placeholder: "Search for products..."
        validation: on_submit
        focused_on_load: false
        width: 100%
        max_width: 600px
        autocomplete: true
        aria_label: "Search for products"

    - search_button:
        visible: true
        type: button
        label: "Search"
        disabled: false
        icon: search_icon
        aria_label: "Submit search"

    - results_list:
        visible: false  # until search performed
        layout: grid
        items_per_page: 10
        min_height: 400px

    - empty_state:
        visible: false  # only when no results
        message: "No products found"
        illustration: true
        suggestions: true

    - pagination:
        visible: false  # only if results > 10
        position: bottom_center
        show_page_numbers: true
        show_prev_next: true

    - filter_panel:
        visible: false  # shown after search
        position: left_sidebar
        collapsible: true
        filters:
          - category_filter
          - price_filter
          - rating_filter

    - sort_dropdown:
        visible: false  # shown after search
        position: top_right
        default_value: "Relevance"
        options:
          - Relevance
          - Price: Low to High
          - Price: High to Low
          - Rating
          - Newest

    - filter_pills:
        visible: false  # shown when filters active
        position: above_results
        dismissible: true

    - autocomplete_dropdown:
        visible: false  # shown while typing
        max_items: 8
        position: below_input
        z_index: 1000

  states:
    initial:
      - search_input: visible, enabled, empty
      - search_button: visible, enabled
      - results_list: hidden
      - filter_panel: hidden
      - sort_dropdown: hidden
      - pagination: hidden

    searching:
      - search_button: shows spinner, disabled
      - search_input: disabled
      - results_list: shows skeleton loaders (10 items)
      - loading_message: "Searching..."
      - filter_panel: disabled
      - sort_dropdown: disabled

    results_found:
      - results_list: visible, populated with products
      - pagination: visible if results > 10
      - filter_panel: visible, expanded
      - sort_dropdown: visible
      - empty_state: hidden
      - result_count: "X products found"

    no_results:
      - results_list: hidden
      - empty_state: visible with message and illustration
      - suggestions: visible with trending searches
      - filter_panel: hidden
      - sort_dropdown: hidden
      - pagination: hidden

    error:
      - error_message:
          color: red
          position: above_results
          dismissible: true
          duration: 5000ms
          text: "Something went wrong. Please try again."
      - results_list: hidden
      - retry_button: visible

    filtering:
      - results_list: shows skeleton loaders
      - filter_panel: active filter highlighted
      - filter_pills: shows active filters
      - result_count: updating

    autocomplete_active:
      - autocomplete_dropdown: visible below input
      - autocomplete_items: top 5 products + top 3 categories
      - matching_text: bold
      - keyboard_navigation: arrow keys select, enter confirms

  responsive:
    mobile:  # <640px
      layout: single_column
      search_input:
        width: 100%
        position: fixed_top (when overlay active)
      search_button:
        width: 48px  # icon only, label hidden
      results_list:
        layout: single_column
        items_per_page: 5
        card_spacing: 12px
      filter_panel:
        position: bottom_sheet_modal
        visible: false  # collapsed by default
        trigger: "Filters" button
      sort_dropdown:
        width: 100%
        position: sticky_top
      pagination:
        show_page_numbers: false  # prev/next only
      autocomplete_dropdown:
        width: 100vw
        position: fullscreen_overlay

    tablet:  # 640-1024px
      layout: single_column
      search_input:
        width: 100%
        max_width: 500px
      results_list:
        layout: grid_2_columns
        items_per_page: 10
        card_spacing: 16px
      filter_panel:
        position: left_sidebar
        width: 200px
        collapsible: true
      sort_dropdown:
        width: 200px
      pagination:
        show_page_numbers: true

    desktop:  # >1024px
      layout: two_column
      search_input:
        width: 600px
        centered: true
      results_list:
        layout: grid_3_columns
        items_per_page: 12
        card_spacing: 24px
      filter_panel:
        position: left_sidebar
        width: 250px
        always_visible: true
      sort_dropdown:
        width: 200px
        position: top_right
      pagination:
        show_page_numbers: true
        show_first_last: true

  accessibility:
    - search_input:
        aria_label: "Search for products"
        aria_describedby: "search-help-text"
    - search_button:
        aria_label: "Submit search query"
    - results_list:
        role: "region"
        aria_label: "Search results"
    - empty_state:
        role: "status"
        aria_live: "polite"
    - error_message:
        role: "alert"
        aria_live: "assertive"
    - filter_panel:
        role: "region"
        aria_label: "Filter options"
    - autocomplete_dropdown:
        role: "listbox"
        aria_label: "Search suggestions"
    - pagination:
        role: "navigation"
        aria_label: "Search results pages"
    - keyboard_navigation:
        tab_order: "search_input → search_button → filter_panel → sort_dropdown → results_list → pagination"
        search_input_keys: "Enter = submit, Escape = clear, ArrowDown = open autocomplete"
        results_list_keys: "Tab = navigate items, Enter = open product"
        autocomplete_keys: "ArrowDown/Up = navigate suggestions, Enter = select, Escape = close"

  interactions:
    - search_submit:
        trigger: "search_button click OR Enter key in search_input"
        validation: "search_input must not be empty"
        action: "navigate to /search?q={query}"
        loading_state: 500ms max

    - autocomplete_trigger:
        trigger: "search_input typing"
        debounce: 300ms
        min_characters: 2
        action: "show autocomplete_dropdown with top 8 matches"

    - filter_apply:
        trigger: "filter checkbox change"
        action: "refresh results with filter params"
        loading_state: 300ms max
        url_update: "add ?category=X or &price=Y"

    - sort_change:
        trigger: "sort_dropdown selection"
        action: "reorder results by selected criteria"
        loading_state: 300ms max
        url_update: "add/update ?sort=X"

    - pagination_click:
        trigger: "pagination button click"
        action: "load next/previous page"
        loading_state: 400ms max
        scroll_behavior: "scroll to top of results"
        url_update: "add/update ?page=X"

  performance:
    - initial_search: "<500ms"
    - filter_update: "<300ms"
    - sort_update: "<300ms"
    - pagination: "<400ms"
    - autocomplete_response: "<300ms"
    - skeleton_display: "immediate"
```

---

## Key Patterns in This Example

### 1. Gherkin for UI Behavior
- **User actions**: "I enter", "I click", "I press"
- **Visual feedback**: "appears", "shows", "is highlighted"
- **Timing**: "within 500ms", "after 3000ms"
- **State changes**: "is disabled", "is hidden", "scrolls to top"
- **URL updates**: navigation and query parameters
- **Keyboard interactions**: arrow keys, Enter, Escape

### 2. Visual YAML for UI Specifications
- **Elements section**: All interactive and display elements
- **States section**: Initial, searching, results_found, no_results, error, filtering, autocomplete_active
- **Responsive section**: Mobile, tablet, desktop breakpoints with layout changes
- **Accessibility section**: ARIA labels, roles, keyboard navigation
- **Interactions section**: Triggers, validations, actions, timing
- **Performance section**: Target timing for each interaction

### 3. Complementary Formats
- **Gherkin**: Describes behavior and user journeys
- **Visual YAML**: Describes appearance and UI state

Together, they provide complete specification:
- Gherkin → Test scenarios for Cypress, Playwright, Selenium
- Visual YAML → Storybook stories, visual regression tests, UI component specs

### 4. Responsive Specifications
Each breakpoint defines:
- Layout changes (single_column, grid_2_columns, grid_3_columns)
- Element positioning (left_sidebar, bottom_sheet_modal)
- Width and spacing adjustments
- Visibility toggles (some elements hidden on mobile)

### 5. Accessibility Requirements
Every interactive element has:
- ARIA label for screen readers
- ARIA role for non-semantic elements
- ARIA live regions for dynamic content
- Keyboard navigation paths and shortcuts

---

## Usage in Development

### Gherkin → Automated Tests

```python
# Behave + Playwright implementation
@when('I enter "{text}" in "{field}"')
def step_enter_text(context, text, field):
    context.page.fill(f'[aria-label="{field}"]', text)

@then('search results appear within {ms:d}ms')
def step_results_appear(context, ms):
    start = time.time()
    context.page.wait_for_selector('[role="region"][aria-label="Search results"]')
    elapsed = (time.time() - start) * 1000
    assert elapsed < ms, f"Results took {elapsed}ms, expected <{ms}ms"

@then('each result shows product image, title, price')
def step_result_structure(context):
    results = context.page.query_selector_all('.product-card')
    for result in results:
        assert result.query_selector('img'), "Missing product image"
        assert result.query_selector('.title'), "Missing title"
        assert result.query_selector('.price'), "Missing price"
```

### Visual YAML → Storybook Stories

```typescript
// Storybook story generated from YAML
export const SearchInitialState: Story = {
  args: {
    searchInput: { visible: true, enabled: true, value: "" },
    searchButton: { visible: true, enabled: true },
    resultsList: { visible: false },
    filterPanel: { visible: false },
  },
};

export const SearchWithResults: Story = {
  args: {
    searchInput: { visible: true, enabled: true, value: "laptop" },
    resultsList: {
      visible: true,
      items: mockProducts.slice(0, 10),
      layout: "grid"
    },
    filterPanel: { visible: true, expanded: true },
    sortDropdown: { visible: true, value: "Relevance" },
    pagination: { visible: true, currentPage: 1, totalPages: 2 },
  },
};

export const SearchNoResults: Story = {
  args: {
    searchInput: { visible: true, enabled: true, value: "nonexistent" },
    emptyState: {
      visible: true,
      message: "No products found",
      showIllustration: true,
      showSuggestions: true
    },
  },
};
```

### Visual YAML → Visual Regression Tests

```typescript
// Percy visual test configuration from YAML responsive specs
describe('Product Search Visual Regression', () => {
  test('mobile layout', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // mobile
    await page.goto('/search?q=laptop');
    await percySnapshot(page, 'Search Results - Mobile', {
      widths: [375],
      minHeight: 667,
    });
  });

  test('tablet layout', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // tablet
    await page.goto('/search?q=laptop');
    await percySnapshot(page, 'Search Results - Tablet', {
      widths: [768],
    });
  });

  test('desktop layout', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 }); // desktop
    await page.goto('/search?q=laptop');
    await percySnapshot(page, 'Search Results - Desktop', {
      widths: [1440],
    });
  });
});
```

---

## Comparison: Before vs After

### Before (Table Format)
```markdown
| AS-2A | HAPPY_PATH | user on homepage | enters search term, clicks search | results appear | YES | 0.95 |
```

### After (Gherkin + Visual YAML)

**Gherkin** for behavior:
```gherkin
Scenario: AS-2A - Search with results found [HAPPY_PATH] [Confidence: 0.95]
  Given database contains 15 products matching "laptop"
  When I enter "laptop" in "search input"
  And I click "Search" button
  Then search results appear within 500ms
  And results list shows 10 items
  And each result shows product image, title, price
```

**Visual YAML** for UI spec:
```yaml
product_search_page:
  elements:
    - search_input: {visible: true, type: search, placeholder: "Search..."}
    - results_list: {layout: grid, items_per_page: 10}
  states:
    results_found:
      - results_list: visible, populated
      - pagination: visible if results > 10
  responsive:
    mobile: {layout: single_column, items_per_page: 5}
    desktop: {layout: grid_3_columns, items_per_page: 12}
```

**Advantages**:
- Executable by BDD frameworks (Cucumber, Playwright, Cypress)
- Clear user interactions and timing expectations
- Complete UI state specifications (elements, states, responsive)
- Accessibility requirements defined
- Can generate: Playwright tests, Storybook stories, visual regression tests
- Structured format enables automation and code generation
