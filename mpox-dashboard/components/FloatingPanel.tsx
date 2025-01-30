import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface FloatingPanelProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function FloatingPanel({
  title,
  children,
  className,
}: FloatingPanelProps) {
  return (
    <Card
      className={`backdrop-blur-md bg-white/70 shadow-xl ${className || ""}`}
    >
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}
