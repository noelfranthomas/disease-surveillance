// components/Chart.tsx
"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";

const timeChartConfig = {
  dailyCases: {
    label: "Daily Cases",
    color: "hsl(var(--chart-1))",
  },
} as const;

const barChartConfig = {
  january: { label: "Jan", color: "hsl(var(--chart-1))" },
  february: { label: "Feb", color: "hsl(var(--chart-2))" },
  march: { label: "Mar", color: "hsl(var(--chart-3))" },
  april: { label: "Apr", color: "hsl(var(--chart-4))" },
  may: { label: "May", color: "hsl(var(--chart-5))" },
  june: { label: "Jun", color: "hsl(var(--chart-2))" },
} as const;

const regionChartConfig = {
  regionA: { label: "Region A", color: "hsl(var(--chart-1))" },
  regionB: { label: "Region B", color: "hsl(var(--chart-2))" },
  regionC: { label: "Region C", color: "hsl(var(--chart-3))" },
  regionD: { label: "Region D", color: "hsl(var(--chart-4))" },
} as const;

const timeData = [
  { date: "2024-01-01", dailyCases: 20 },
  { date: "2024-01-02", dailyCases: 30 },
  { date: "2024-01-03", dailyCases: 25 },
  { date: "2024-01-04", dailyCases: 40 },
  { date: "2024-01-05", dailyCases: 35 },
  { date: "2024-01-06", dailyCases: 50 },
  { date: "2024-01-07", dailyCases: 45 },
];

const monthlyData = [
  {
    month: "January",
    january: 186,
    february: 305,
    march: 237,
    april: 73,
    may: 209,
    june: 214,
  },
];

const regionData = [
  { name: "Region A", value: 400 },
  { name: "Region B", value: 300 },
  { name: "Region C", value: 200 },
  { name: "Region D", value: 100 },
];

interface ChartCommonProps {
  chartProps?: Partial<
    React.ComponentProps<typeof LineChart> | typeof BarChart | typeof PieChart
  >;
}

export function TimeSeriesChart({ chartProps }: ChartCommonProps) {
  return (
    <ChartContainer config={timeChartConfig} className="w-full h-full">
      <LineChart data={timeData} accessibilityLayer {...chartProps}>
        <CartesianGrid vertical={false} strokeDasharray="3 3" />
        <XAxis
          dataKey="date"
          tickLine={false}
          tickMargin={10}
          axisLine={false}
          tickFormatter={(value: string) => value.slice(5)}
        />
        <YAxis tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Line
          type="monotone"
          dataKey="dailyCases"
          stroke="var(--color-dailyCases)"
          strokeWidth={2}
          dot={true}
        />
      </LineChart>
    </ChartContainer>
  );
}

export function MonthlyBarChart({ chartProps }: ChartCommonProps) {
  return (
    <ChartContainer config={barChartConfig} className="w-full h-full">
      <BarChart data={monthlyData} accessibilityLayer {...chartProps}>
        <CartesianGrid vertical={false} strokeDasharray="3 3" />
        <XAxis
          dataKey="month"
          tickLine={false}
          tickMargin={10}
          axisLine={false}
          tickFormatter={(value: string) => value.slice(0, 3)}
        />
        <YAxis tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent nameKey="month" />} />
        <Bar dataKey="january" fill="var(--color-january)" radius={4} />
        <Bar dataKey="february" fill="var(--color-february)" radius={4} />
        <Bar dataKey="march" fill="var(--color-march)" radius={4} />
        <Bar dataKey="april" fill="var(--color-april)" radius={4} />
        <Bar dataKey="may" fill="var(--color-may)" radius={4} />
        <Bar dataKey="june" fill="var(--color-june)" radius={4} />
      </BarChart>
    </ChartContainer>
  );
}

export function RegionalPieChart({ chartProps }: ChartCommonProps) {
  return (
    <ChartContainer
      config={regionChartConfig}
      className="w-full h-full flex items-center justify-center"
    >
      <PieChart accessibilityLayer {...chartProps}>
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent nameKey="name" />} />
        <Pie
          data={regionData}
          dataKey="value"
          nameKey="name"
          innerRadius={50}
          outerRadius={80}
          paddingAngle={3}
        >
          {regionData.map((entry, index) => {
            const colors = [
              "var(--color-regionA)",
              "var(--color-regionB)",
              "var(--color-regionC)",
              "var(--color-regionD)",
            ];
            return (
              <Cell
                key={`cell-${index}`}
                fill={colors[index % colors.length]}
              />
            );
          })}
        </Pie>
      </PieChart>
    </ChartContainer>
  );
}
