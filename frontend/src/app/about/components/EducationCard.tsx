import { Card, CardContent, Typography, Avatar, Box } from '@mui/material';
import React from 'react';
import Image from 'next/image';

interface EducationCardProps {
  onClick: () => void;
  logo?: string;
  degree: string;
  school: string;
}

const EducationCard: React.FC<EducationCardProps> = ({ onClick, logo, degree, school }) => (
  <Card
    onClick={onClick}
    sx={{
      bgcolor: 'rgba(98, 96, 108, 0.85)',
      color: 'rgba(255,255,255,0.85)',
      borderRadius: '10px',
      boxShadow: 6,
      p: 0,
      cursor: 'pointer',
      transition: 'transform 0.2s, box-shadow 0.2s, background 0.2s',
      '&:hover': {
        transform: 'translateY(-4px)',
        boxShadow: 10,
        bgcolor: 'rgba(116, 114, 129, 0.91)',
      },
    }}
  >
    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      {logo && (
        logo.endsWith('.svg') ? (
          <Image
            src={logo}
            alt={school}
            width={48}
            height={48}
            style={{ marginRight: 16, display: 'block', background: 'transparent', objectFit: 'contain', borderRadius: 6, maxWidth: 80 }}
            unoptimized
          />
        ) : (
          <Avatar src={logo} alt={school} sx={{ width: 48, height: 48, mr: 2 }} />
        )
      )}
      <Box>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 0.5 }}>
          {degree}
        </Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
          {school}
        </Typography>
      </Box>
    </CardContent>
  </Card>
);

export default EducationCard; 