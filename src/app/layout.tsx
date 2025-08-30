"use client"

import { Inter } from 'next/font/google'
import './globals.css'
import { AccessibilityProvider } from '../providers/AccessibilityProvider'
import { ThemeProvider } from '../providers/ThemeProvider'
import { Toaster } from '../components/ui/sonner'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <head>
        <title>NeuroDemon - AI-Powered Neurodivergent-Friendly Penetration Testing</title>
        <meta name="description" content="Professional penetration testing application designed specifically for neurodivergent cybersecurity professionals. Features AI guidance, ADHD-friendly workflows, and comprehensive accessibility support." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#1e293b" />
        
        <meta name="accessibility-features" content="ARIA, keyboard-navigation, screen-reader-compatible, focus-management" />
        <meta name="neurodivergent-friendly" content="ADHD, autism, anxiety, OCD, PTSD support" />
        
        <link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
        
        <meta httpEquiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline';" />
        
        <meta name="robots" content="noindex, nofollow" />
        <meta name="legal-notice" content="For authorized penetration testing only. Unauthorized use prohibited." />
      </head>
      <body className="font-sans antialiased bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 min-h-screen">
        <ThemeProvider>
          <AccessibilityProvider>
            <div className="flex flex-col min-h-screen">
              <main className="flex-1 relative">
                <div className="container mx-auto px-4 py-6">
                  {children}
                </div>
              </main>
              
              <footer className="bg-slate-100 dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 mt-auto">
                <div className="container mx-auto px-4 py-4">
                  <div className="flex flex-col md:flex-row justify-between items-center space-y-2 md:space-y-0">
                    <div className="flex items-center space-x-4 text-sm text-slate-600 dark:text-slate-400">
                      <span>⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY</span>
                      <span>•</span>
                      <span>NeuroDemon v1.0.0</span>
                    </div>
                    <div className="flex items-center space-x-4 text-sm">
                      <button className="text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors">
                        Accessibility Settings
                      </button>
                      <button className="text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors">
                        Legal Info
                      </button>
                    </div>
                  </div>
                </div>
              </footer>
            </div>
            <Toaster />
          </AccessibilityProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}