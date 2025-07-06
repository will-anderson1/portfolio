'use client';

import { useEffect } from 'react';
import particlesJson from '@/app/resources/particles.json';
import { useParticles } from '@/contexts/ParticleContext';

declare global {
  interface Window {
    particlesJS: unknown;
    pJSDom: unknown[];
  }
}

export default function ParticlesBackground() {
  const { particlesEnabled } = useParticles();
  
  useEffect(() => {
    if (!particlesEnabled) {
      // Destroy particles when disabled
      if (window.pJSDom && window.pJSDom[0]) {
        window.pJSDom[0].pJS.fn.vendors.destroypJS();
        window.pJSDom = [];
      }
      return;
    }

    // Load particles.js script dynamically
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js';
    script.async = true;
    
    script.onload = () => {
      if (window.particlesJS) {
        window.particlesJS('particles-js', particlesJson);
      }
    };

    document.head.appendChild(script);

    return () => {
      // Cleanup
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, [particlesEnabled]);

  if (!particlesEnabled) {
    return (
      <div 
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: -1,
          backgroundColor: '#2F373B'
        }}
      />
    );
  }

  return (
    <div 
      id="particles-js" 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        backgroundColor: '#2F373B'
      }}
    />
  );
} 