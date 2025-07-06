'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ParticleContextType {
  particlesEnabled: boolean;
  toggleParticles: () => void;
}

const ParticleContext = createContext<ParticleContextType | undefined>(undefined);

export function ParticleProvider({ children }: { children: ReactNode }) {
  const [particlesEnabled, setParticlesEnabled] = useState(true);

  const toggleParticles = () => {
    setParticlesEnabled(prev => !prev);
  };

  return (
    <ParticleContext.Provider value={{ particlesEnabled, toggleParticles }}>
      {children}
    </ParticleContext.Provider>
  );
}

export function useParticles() {
  const context = useContext(ParticleContext);
  if (context === undefined) {
    throw new Error('useParticles must be used within a ParticleProvider');
  }
  return context;
} 