import Image from "next/image";
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar } from '@mui/material';

export default function Home() {
  return (
    <div style={{ zIndex: 2 }} className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center pt-8 pb-4 gap-6 sm:pt-16 sm:pb-8 font-[family-name:var(--font-geist-sans)]">

      {/* Centered Avatar */}
      <div className="row-start-2 flex flex-col items-center justify-center mt-0">
        <Avatar
          alt="Will Anderson"
          src="/avatar.png"
          sx={{ width: 400, height: 400, boxShadow: 10, mb: 1 }}
        />
        {/* Name and Title */}
        <div className="flex flex-col items-center mt-2">
          <div style={{ fontSize: 32, fontWeight: 700, letterSpacing: 1, lineHeight: 1.2 }}>Will Anderson</div>
          <div style={{ fontSize: 20, fontWeight: 400, color: 'rgba(168, 168, 168, 0.89)', marginTop: 8, textAlign: 'center', lineHeight: 1.3 }}>
            Fullstack Software Engineer<br />MS Computer Science, BS Computer Science + Mathematics Minor
          </div>
        </div>
      </div>

      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://www.linkedin.com/in/will-anderson0/"
          target="_blank"
          rel="noopener noreferrer"
        >
          <LinkedInIcon sx={{ fontSize: 20, color: '#0077B5' }} />
          LinkedIn
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://github.com/will-anderson1"
          target="_blank"
          rel="noopener noreferrer"
        >
          <GitHubIcon sx={{ fontSize: 20, color: '#181717' }} />
          GitHub
        </a>
      </footer>
    </div>
  );
}
