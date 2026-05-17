"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Boxes, Calculator, Gauge, Map, Route } from "lucide-react";

const links = [
  { href: "/", label: "Home", icon: Gauge },
  { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { href: "/yard-simulator", label: "Yard", icon: Map },
  { href: "/retrieval", label: "Retrieval", icon: Route },
  { href: "/pricing", label: "Pricing", icon: Calculator },
  { href: "/methodology", label: "Method", icon: Boxes }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <Link href="/" className="brand">
            <span className="brand-mark"><Boxes size={18} /></span>
            <span>YardOps Intelligence</span>
          </Link>
          <nav className="nav" aria-label="Primary navigation">
            {links.map((link) => {
              const Icon = link.icon;
              const active = pathname === link.href;
              return (
                <Link key={link.href} href={link.href} className={`nav-link ${active ? "active" : ""}`}>
                  <Icon size={16} />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
