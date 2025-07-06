import { Card, CardContent, Typography, Avatar, Box } from '@mui/material';
import React from 'react';

interface WorkCardProps {
  onClick: () => void;
  logo?: string;
  position: string;
  company: string;
}

const WorkCard: React.FC<WorkCardProps> = ({ onClick, logo, position, company }) => (
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
          <img
            src={logo}
            alt={company}
            style={{
              height: 40,
              width: 'auto',
              marginLeft: 16,
              borderRadius: 6,
              objectFit: 'contain',
              padding: 2,
              maxWidth: 80,
              background: 'transparent',
              display: 'block',
            }}
          />
        ) : (
          <img
            src={logo}
            alt={company}
            style={{
              height: 40,
              width: 'auto',
              marginLeft: 16,
              borderRadius: 6,
              objectFit: 'contain',
              padding: 2,
              maxWidth: 80,
              background: 'transparent',
              display: 'block',
            }}
          />
        )
      )}
      <Box>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 0.5 }}>
          {position}
        </Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
          {company}
        </Typography>
      </Box>
    </CardContent>
  </Card>
);

export default WorkCard; 