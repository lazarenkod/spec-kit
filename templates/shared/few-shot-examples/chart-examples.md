# Chart Examples (Few-Shot)

## Example 1: Line Chart with Multiple Series

### Specification
- Purpose: Display trend data over time with multiple data series
- States: Loading, populated, empty, error
- Accessibility: Data table alternative, ARIA labels, keyboard navigation

### Code
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { month: 'Jan', revenue: 4000, expenses: 2400, profit: 1600 },
  { month: 'Feb', revenue: 3000, expenses: 1398, profit: 1602 },
  { month: 'Mar', revenue: 2000, expenses: 9800, profit: -7800 },
  { month: 'Apr', revenue: 2780, expenses: 3908, profit: -1128 },
  { month: 'May', revenue: 1890, expenses: 4800, profit: -2910 },
  { month: 'Jun', revenue: 2390, expenses: 3800, profit: -1410 },
];

export function RevenueLineChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Financial Performance</CardTitle>
        <CardDescription>Revenue, expenses, and profit over time</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="month"
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              tickFormatter={(value) => `$${value / 1000}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--popover))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 'var(--radius)',
              }}
              formatter={(value: number) => `$${value.toLocaleString()}`}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--primary))' }}
              activeDot={{ r: 6 }}
            />
            <Line
              type="monotone"
              dataKey="expenses"
              stroke="hsl(var(--destructive))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--destructive))' }}
            />
            <Line
              type="monotone"
              dataKey="profit"
              stroke="hsl(var(--success))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--success))' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Responsive container adapts to parent width
- Token-based colors (primary, destructive, success)
- Grid lines for easier reading
- Formatted Y-axis ($Xk notation)
- Interactive tooltip with formatted values
- Clear legend for series identification
- Proper margins to prevent label cutoff

---

## Example 2: Bar Chart with Comparison

### Specification
- Purpose: Compare categorical data with grouped bars
- States: Loading skeleton, populated, empty state
- Accessibility: Data labels, high contrast colors

### Code
```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { product: 'Product A', q1: 4000, q2: 3000, q3: 5000, q4: 4500 },
  { product: 'Product B', q1: 3000, q2: 4500, q3: 3500, q4: 6000 },
  { product: 'Product C', q1: 2000, q2: 2500, q3: 3000, q4: 3500 },
  { product: 'Product D', q1: 2780, q2: 3908, q3: 4500, q4: 4200 },
];

export function QuarterlySalesChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quarterly Sales by Product</CardTitle>
        <CardDescription>Q1-Q4 2024 comparison</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="product"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              tickFormatter={(value) => `$${value / 1000}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--popover))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 'var(--radius)',
              }}
              formatter={(value: number) => `$${value.toLocaleString()}`}
            />
            <Legend />
            <Bar dataKey="q1" fill="hsl(var(--chart-1))" radius={[4, 4, 0, 0]} />
            <Bar dataKey="q2" fill="hsl(var(--chart-2))" radius={[4, 4, 0, 0]} />
            <Bar dataKey="q3" fill="hsl(var(--chart-3))" radius={[4, 4, 0, 0]} />
            <Bar dataKey="q4" fill="hsl(var(--chart-4))" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Grouped bars for easy comparison across quarters
- Rounded top corners for modern aesthetic
- Chart color tokens (--chart-1 through --chart-4)
- Clear categorical X-axis labels
- Formatted currency values in tooltip
- Adequate spacing between bar groups

---

## Example 3: Pie Chart with Percentage Labels

### Specification
- Purpose: Show proportional distribution of categories
- States: Loading, populated, empty (no data message)
- Accessibility: Labeled segments, data table alternative

### Code
```tsx
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { name: 'Direct', value: 4500, color: 'hsl(var(--chart-1))' },
  { name: 'Organic', value: 3200, color: 'hsl(var(--chart-2))' },
  { name: 'Social', value: 2100, color: 'hsl(var(--chart-3))' },
  { name: 'Referral', value: 1800, color: 'hsl(var(--chart-4))' },
  { name: 'Email', value: 900, color: 'hsl(var(--chart-5))' },
];

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? 'start' : 'end'}
      dominantBaseline="central"
      className="text-xs font-medium"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

export function TrafficSourcesChart() {
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Traffic Sources</CardTitle>
        <CardDescription>
          Total sessions: {total.toLocaleString()}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--popover))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 'var(--radius)',
              }}
              formatter={(value: number) => [
                `${value.toLocaleString()} sessions`,
                '',
              ]}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value, entry: any) => {
                const percentage = ((entry.payload.value / total) * 100).toFixed(1);
                return `${value} (${percentage}%)`;
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Percentage labels directly on pie segments
- Legend shows both name and percentage
- Tooltip with absolute values
- Total count in header for context
- Token-based colors for consistency
- White text on colored segments for contrast

---

## Example 4: Area Chart with Gradient Fill

### Specification
- Purpose: Show cumulative metrics over time with visual emphasis
- States: Loading, populated, empty
- Accessibility: Gradient doesn't obscure data, clear axis labels

### Code
```tsx
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { date: 'Jan 1', users: 1200 },
  { date: 'Jan 8', users: 1500 },
  { date: 'Jan 15', users: 1800 },
  { date: 'Jan 22', users: 2200 },
  { date: 'Jan 29', users: 2800 },
  { date: 'Feb 5', users: 3200 },
  { date: 'Feb 12', users: 3600 },
];

export function UserGrowthChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>User Growth</CardTitle>
        <CardDescription>Cumulative active users</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="hsl(var(--primary))"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="hsl(var(--primary))"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="date"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              className="text-xs"
            />
            <YAxis
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              tickFormatter={(value) => `${value / 1000}k`}
              className="text-xs"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--popover))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 'var(--radius)',
              }}
              formatter={(value: number) => [
                `${value.toLocaleString()} users`,
                'Total',
              ]}
            />
            <Area
              type="monotone"
              dataKey="users"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorUsers)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Gradient fill emphasizes area under curve
- Linear gradient from 80% to 10% opacity
- Smooth monotone interpolation
- Token-based primary color for consistency
- Clear cumulative metric presentation

---

## Example 5: Composed Chart (Bar + Line Combination)

### Specification
- Purpose: Show multiple metrics with different scales on same chart
- States: Loading, populated, sync tooltip across both axes
- Accessibility: Dual Y-axis labels, clear legend differentiation

### Code
```tsx
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { month: 'Jan', sales: 4000, conversion: 2.4 },
  { month: 'Feb', sales: 3000, conversion: 1.8 },
  { month: 'Mar', sales: 5000, conversion: 3.2 },
  { month: 'Apr', sales: 4500, conversion: 2.8 },
  { month: 'May', sales: 6000, conversion: 3.5 },
  { month: 'Jun', sales: 5500, conversion: 3.1 },
];

export function SalesConversionChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Sales & Conversion Rate</CardTitle>
        <CardDescription>Monthly performance metrics</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <ComposedChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="month"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
            />
            <YAxis
              yAxisId="left"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              tickFormatter={(value) => `$${value / 1000}k`}
              label={{
                value: 'Sales',
                angle: -90,
                position: 'insideLeft',
                style: { fill: 'hsl(var(--muted-foreground))' },
              }}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              tick={{ fill: 'hsl(var(--muted-foreground))' }}
              tickFormatter={(value) => `${value}%`}
              label={{
                value: 'Conversion Rate',
                angle: 90,
                position: 'insideRight',
                style: { fill: 'hsl(var(--muted-foreground))' },
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--popover))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 'var(--radius)',
              }}
              formatter={(value: number, name: string) => {
                if (name === 'sales') return [`$${value.toLocaleString()}`, 'Sales'];
                return [`${value}%`, 'Conversion'];
              }}
            />
            <Legend />
            <Bar
              yAxisId="left"
              dataKey="sales"
              fill="hsl(var(--primary))"
              radius={[4, 4, 0, 0]}
              barSize={40}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="conversion"
              stroke="hsl(var(--success))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--success))', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

### Why This Works
- Dual Y-axes for different scales (sales $, conversion %)
- Bar + line combination shows relationship between metrics
- Axis labels clarify which metric uses which scale
- Synced tooltip shows both values
- Different colors distinguish metric types
- Appropriate bar width (not too thick/thin)
