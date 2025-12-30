# Feature to Screens Mapping Algorithm

Systematic approach to derive screen inventory from concept.md feature hierarchy.

## Input: Feature Structure from Concept

```yaml
feature:
  id: EPIC-001.F01
  name: User Dashboard
  stories:
    - id: S01
      name: View activity summary
      acceptance:
        - GIVEN logged in user
        - WHEN viewing dashboard
        - THEN shows recent activity
    - id: S02
      name: Quick actions panel
      acceptance:
        - GIVEN logged in user
        - WHEN clicking quick action
        - THEN performs action
```

## Mapping Algorithm

### Step 1: Story → Primary Screen

```text
FOR each story IN feature.stories:

  1. ANALYZE story name and acceptance criteria
  2. DETERMINE screen type:

     | Story Pattern | Screen Type |
     |---------------|-------------|
     | "View X", "See X", "Display X" | Detail/Dashboard screen |
     | "Create X", "Add X", "New X" | Creation form/wizard |
     | "Edit X", "Update X", "Modify X" | Edit form |
     | "Delete X", "Remove X" | Confirmation modal |
     | "Search X", "Find X", "Filter X" | List with filters |
     | "Select X", "Choose X" | Selection interface |
     | "Configure X", "Set X" | Settings panel |
     | "Export X", "Download X" | Export dialog |
     | "Import X", "Upload X" | Import wizard |
     | "Approve X", "Review X" | Review/approval flow |

  3. OUTPUT: primary_screen for this story
```

### Step 2: Identify Screen Modifiers

```text
FOR each story.acceptance_criteria:

  1. PARSE GIVEN/WHEN/THEN structure
  2. EXTRACT state modifiers:

     | Criteria Pattern | Screen State/Modifier |
     |------------------|----------------------|
     | "GIVEN no X exists" | Empty state |
     | "GIVEN X is loading" | Loading state |
     | "WHEN action fails" | Error state |
     | "THEN shows success" | Success state |
     | "WHEN on mobile" | Mobile variant |
     | "GIVEN first-time user" | Onboarding overlay |
     | "WHEN X exceeds limit" | Pagination/virtualization |

  3. OUTPUT: state_variations for this screen
```

### Step 3: Identify Secondary Screens

```text
FOR each story:

  1. LOOK FOR implicit screens:

     | Story Element | Secondary Screen |
     |---------------|------------------|
     | Form submission | Confirmation dialog |
     | Destructive action | Warning modal |
     | Multi-step process | Wizard steps |
     | Detail link | Detail view |
     | Settings reference | Settings panel |
     | Help reference | Help overlay |

  2. OUTPUT: secondary_screens
```

### Step 4: Map Routes

```text
FOR each screen:

  1. GENERATE route based on:
     - Feature ID → base path
     - Screen type → action suffix
     - Parameters → dynamic segments

     | Screen Type | Route Pattern |
     |-------------|---------------|
     | List | /features/{feature}/ |
     | Detail | /features/{feature}/:id |
     | Create | /features/{feature}/new |
     | Edit | /features/{feature}/:id/edit |
     | Settings | /features/{feature}/settings |

  2. OUTPUT: route for this screen
```

## Output: Screen Inventory Table

```markdown
## Screen Inventory for {Feature Name}

| Screen | Story | Route | States | Components |
|--------|-------|-------|--------|------------|
| Dashboard | S01, S02 | /dashboard | default, loading, empty | ActivityFeed, QuickActions |
| Activity Detail | S01 | /dashboard/activity/:id | default, loading | ActivityCard, Timeline |
| Quick Action Modal | S02 | /dashboard (modal) | default, loading, success, error | ActionForm, Toast |
```

## Example: Full Mapping

### Input (from concept.md)

```yaml
EPIC-001.F01: User Dashboard
  S01: View activity summary
    - GIVEN logged in user
    - WHEN viewing dashboard
    - THEN shows last 10 activities
    - AND shows summary stats
  S02: Quick actions panel
    - GIVEN logged in user
    - WHEN clicking quick action
    - THEN opens action modal
    - AND submits action
  S03: Empty state experience
    - GIVEN new user with no activity
    - WHEN viewing dashboard
    - THEN shows welcome message
    - AND shows getting started guide
```

### Output

```markdown
| Screen | Story | Route | States | Priority |
|--------|-------|-------|--------|----------|
| Dashboard Main | S01, S02, S03 | /dashboard | default, loading, empty | P0 |
| Activity Feed | S01 | /dashboard (section) | default, loading, empty | P0 |
| Stats Summary | S01 | /dashboard (section) | default, loading | P1 |
| Quick Actions Bar | S02 | /dashboard (section) | default | P0 |
| Action Modal | S02 | /dashboard (modal) | default, loading, success, error | P0 |
| Welcome Overlay | S03 | /dashboard (overlay) | default | P1 |
| Getting Started Guide | S03 | /dashboard (panel) | default, completed | P1 |
```

## Integration with Design Process

```text
1. RUN feature-to-screens.md algorithm
2. OUTPUT screen_inventory.md
3. FOR each screen:
     - GENERATE wireframe
     - DEFINE component list
     - SPECIFY states
4. AGGREGATE into feature-design.md
```
