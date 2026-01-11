# Dashboard Examples (Few-Shot)

## Example 1: KPI Dashboard with Cards

### Specification
- Purpose: Display key metrics in a scannable grid layout
- States: Loading, populated, empty state
- Accessibility: Screen reader support for metric changes, ARIA live regions

### Code
```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Users, DollarSign } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string;
  change: number;
  icon: React.ReactNode;
}

function MetricCard({ title, value, change, icon }: MetricCardProps) {
  const isPositive = change >= 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className="text-muted-foreground">{icon}</div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground flex items-center gap-1">
          {isPositive ? (
            <TrendingUp className="h-4 w-4 text-green-600" />
          ) : (
            <TrendingDown className="h-4 w-4 text-red-600" />
          )}
          <span className={isPositive ? 'text-green-600' : 'text-red-600'}>
            {Math.abs(change)}%
          </span>
          <span>from last month</span>
        </p>
      </CardContent>
    </Card>
  );
}

export function KPIDashboard() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        title="Total Revenue"
        value="$45,231"
        change={20.1}
        icon={<DollarSign className="h-4 w-4" />}
      />
      <MetricCard
        title="Active Users"
        value="2,350"
        change={15.3}
        icon={<Users className="h-4 w-4" />}
      />
      <MetricCard
        title="Conversion Rate"
        value="3.24%"
        change={-2.4}
        icon={<TrendingUp className="h-4 w-4" />}
      />
      <MetricCard
        title="Avg. Session"
        value="4m 32s"
        change={8.1}
        icon={<TrendingUp className="h-4 w-4" />}
      />
    </div>
  );
}
```

### Why This Works
- Responsive grid (2 cols → 4 cols on larger screens)
- Consistent card structure with header/content separation
- Visual trend indicators (up/down arrows with color coding)
- Accessible metric labels and live region support
- Icon + text combination for scannability

---

## Example 2: Analytics Dashboard with Chart Grid

### Specification
- Purpose: Display multiple charts in organized layout
- States: Loading, populated, error
- Accessibility: Chart descriptions, keyboard navigation

### Code
```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, BarChart, PieChart } from '@/components/ui/chart';

export function AnalyticsDashboard() {
  return (
    <div className="space-y-4">
      {/* Top section: Large chart */}
      <Card>
        <CardHeader>
          <CardTitle>Revenue Overview</CardTitle>
          <CardDescription>January - June 2024</CardDescription>
        </CardHeader>
        <CardContent className="h-80">
          <LineChart
            data={revenueData}
            xKey="month"
            yKey="revenue"
            className="h-full w-full"
          />
        </CardContent>
      </Card>

      {/* Bottom section: 2-column grid */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top Products</CardTitle>
            <CardDescription>By sales volume</CardDescription>
          </CardHeader>
          <CardContent className="h-64">
            <BarChart
              data={productsData}
              xKey="product"
              yKey="sales"
              className="h-full w-full"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Traffic Sources</CardTitle>
            <CardDescription>By channel</CardDescription>
          </CardHeader>
          <CardContent className="h-64">
            <PieChart
              data={trafficData}
              nameKey="source"
              valueKey="percentage"
              className="h-full w-full"
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

### Why This Works
- Hero chart + supporting charts layout pattern
- Consistent card structure across all charts
- Descriptive titles and subtitles for context
- Fixed heights prevent layout shift during loading
- Responsive 1-column → 2-column grid

---

## Example 3: Real-Time Dashboard with Live Updates

### Specification
- Purpose: Display live metrics with auto-refresh
- States: Connected, disconnected, updating
- Accessibility: Live region announcements, connection status

### Code
```tsx
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Activity } from 'lucide-react';

interface LiveMetric {
  id: string;
  label: string;
  value: number;
  unit: string;
}

export function RealtimeDashboard() {
  const [metrics, setMetrics] = useState<LiveMetric[]>([]);
  const [isConnected, setIsConnected] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate WebSocket updates
      setMetrics([
        { id: '1', label: 'Active Sessions', value: Math.floor(Math.random() * 1000), unit: '' },
        { id: '2', label: 'Requests/sec', value: Math.floor(Math.random() * 500), unit: '' },
        { id: '3', label: 'CPU Usage', value: Math.floor(Math.random() * 100), unit: '%' },
        { id: '4', label: 'Memory', value: Math.floor(Math.random() * 8), unit: 'GB' },
      ]);
      setLastUpdate(new Date());
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4">
      {/* Status bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 animate-pulse text-green-600" />
          <span className="text-sm font-medium">Live</span>
        </div>
        <Badge variant={isConnected ? 'default' : 'destructive'}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </Badge>
        <span className="text-sm text-muted-foreground">
          Updated {lastUpdate.toLocaleTimeString()}
        </span>
      </div>

      {/* Metrics grid with live updates */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4" aria-live="polite">
        {metrics.map((metric) => (
          <Card key={metric.id} className="transition-colors duration-200 hover:bg-accent">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {metric.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {metric.value}
                <span className="text-lg text-muted-foreground ml-1">{metric.unit}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
```

### Why This Works
- Live status indicator (pulsing icon)
- Connection status badge for transparency
- Last update timestamp for confidence
- ARIA live region for screen reader announcements
- Smooth transitions on metric updates
- Hover states for interactivity

---

## Example 4: Dashboard with Filters and Date Range

### Specification
- Purpose: Interactive dashboard with global filters
- States: Loading, filtered, empty results
- Accessibility: Filter labels, keyboard navigation

### Code
```tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CalendarIcon } from 'lucide-react';
import { format } from 'date-fns';

export function FilterableDashboard() {
  const [dateRange, setDateRange] = useState<{ from: Date; to: Date }>();
  const [region, setRegion] = useState<string>('all');
  const [product, setProduct] = useState<string>('all');

  return (
    <div className="space-y-6">
      {/* Filter bar */}
      <Card>
        <CardHeader>
          <CardTitle>Filters</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-4">
          {/* Date range picker */}
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-[280px] justify-start text-left">
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dateRange?.from ? (
                  dateRange.to ? (
                    <>
                      {format(dateRange.from, 'LLL dd, y')} -{' '}
                      {format(dateRange.to, 'LLL dd, y')}
                    </>
                  ) : (
                    format(dateRange.from, 'LLL dd, y')
                  )
                ) : (
                  <span>Pick a date range</span>
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="start">
              <Calendar
                initialFocus
                mode="range"
                selected={dateRange}
                onSelect={setDateRange}
                numberOfMonths={2}
              />
            </PopoverContent>
          </Popover>

          {/* Region filter */}
          <Select value={region} onValueChange={setRegion}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Region" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Regions</SelectItem>
              <SelectItem value="us">United States</SelectItem>
              <SelectItem value="eu">Europe</SelectItem>
              <SelectItem value="asia">Asia Pacific</SelectItem>
            </SelectContent>
          </Select>

          {/* Product filter */}
          <Select value={product} onValueChange={setProduct}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Product" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Products</SelectItem>
              <SelectItem value="pro">Pro</SelectItem>
              <SelectItem value="enterprise">Enterprise</SelectItem>
            </SelectContent>
          </Select>

          {/* Reset button */}
          <Button
            variant="ghost"
            onClick={() => {
              setDateRange(undefined);
              setRegion('all');
              setProduct('all');
            }}
          >
            Reset Filters
          </Button>
        </CardContent>
      </Card>

      {/* Dashboard content (filtered) */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Filtered Metric 1</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$12,345</div>
          </CardContent>
        </Card>
        {/* More metrics... */}
      </div>
    </div>
  );
}
```

### Why This Works
- Grouped filters in dedicated card
- Date range picker with calendar UI
- Select dropdowns for categorical filters
- Clear reset action
- Filters applied immediately (or with Apply button)
- Accessible labels and keyboard navigation

---

## Example 5: Dashboard with Collapsible Sections

### Specification
- Purpose: Organize dashboard into collapsible sections
- States: Expanded, collapsed, loading per section
- Accessibility: Section headings, expand/collapse buttons

### Code
```tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DashboardSection {
  id: string;
  title: string;
  description: string;
  defaultOpen?: boolean;
  content: React.ReactNode;
}

export function CollapsibleDashboard() {
  const [openSections, setOpenSections] = useState<Set<string>>(
    new Set(['overview', 'performance'])
  );

  const toggleSection = (sectionId: string) => {
    setOpenSections((prev) => {
      const next = new Set(prev);
      if (next.has(sectionId)) {
        next.delete(sectionId);
      } else {
        next.add(sectionId);
      }
      return next;
    });
  };

  const sections: DashboardSection[] = [
    {
      id: 'overview',
      title: 'Overview',
      description: 'Key metrics at a glance',
      content: <div className="grid gap-4 md:grid-cols-4">{/* Metric cards */}</div>,
    },
    {
      id: 'performance',
      title: 'Performance',
      description: 'System health and performance metrics',
      content: <div className="grid gap-4 md:grid-cols-2">{/* Charts */}</div>,
    },
    {
      id: 'users',
      title: 'User Analytics',
      description: 'User behavior and engagement',
      content: <div className="space-y-4">{/* User tables */}</div>,
    },
  ];

  return (
    <div className="space-y-4">
      {sections.map((section) => {
        const isOpen = openSections.has(section.id);

        return (
          <Card key={section.id}>
            <Collapsible open={isOpen} onOpenChange={() => toggleSection(section.id)}>
              <CollapsibleTrigger asChild>
                <CardHeader className="cursor-pointer hover:bg-accent/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <CardTitle className="flex items-center gap-2">
                        {section.title}
                      </CardTitle>
                      <p className="text-sm text-muted-foreground">
                        {section.description}
                      </p>
                    </div>
                    <Button variant="ghost" size="sm">
                      {isOpen ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRight className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </CardHeader>
              </CollapsibleTrigger>

              <CollapsibleContent>
                <CardContent className="pt-0">
                  {section.content}
                </CardContent>
              </CollapsibleContent>
            </Collapsible>
          </Card>
        );
      })}
    </div>
  );
}
```

### Why This Works
- Clean collapsible sections with smooth transitions
- Section descriptions for context
- Icon rotation (chevron right → down) indicates state
- Hover state on section headers
- Keyboard accessible (space/enter to toggle)
- Maintains open state in Set for performance
