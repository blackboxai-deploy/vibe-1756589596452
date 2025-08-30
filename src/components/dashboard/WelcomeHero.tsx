"use client"

export function WelcomeHero() {
  return (
    <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-2xl text-white p-8 shadow-lg">
      <div className="max-w-4xl">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Welcome to <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">NeuroDemon</span>
        </h1>
        <p className="text-xl md:text-2xl text-blue-100 mb-6 leading-relaxed">
          The first AI-powered penetration testing platform designed specifically for neurodivergent cybersecurity professionals
        </p>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
            <span className="w-2 h-2 bg-green-400 rounded-full"></span>
            <span className="text-sm font-medium">ADHD Friendly</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
            <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
            <span className="text-sm font-medium">Autism Support</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
            <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
            <span className="text-sm font-medium">AI Powered</span>
          </div>
          <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
            <span className="w-2 h-2 bg-orange-400 rounded-full"></span>
            <span className="text-sm font-medium">Legal Compliant</span>
          </div>
        </div>
      </div>
    </div>
  )
}