'use client';

import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  CardActions,
  Button,
  IconButton,
} from '@mui/material';
import {
  AccessTime,
  Share,
  Info,
  Edit,
} from '@mui/icons-material';

export interface NewsItem {
  id: number;
  title: string;
  excerpt: string;
  image: string;
  author: string;
  date: string;
  tags?: string[];
}

interface NewsCardProps {
  item: NewsItem;
  onInfoClick: (item: NewsItem) => void;
  onCardClick: (item: NewsItem) => void;
}

const NewsCard: React.FC<NewsCardProps> = ({ item, onInfoClick, onCardClick }) => {
  const handleShare = (title: string) => {
    if (navigator.share) {
      navigator.share({
        title: title,
        text: `Check out this article: ${title}`,
        url: window.location.href,
      });
    } else {
      // Fallback for browsers that don't support Web Share API
      navigator.clipboard.writeText(`${title} - ${window.location.href}`);
      alert('Link copied to clipboard!');
    }
  };

  return (
    <Card 
      onClick={() => onCardClick(item)}
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        bgcolor: 'rgba(98, 96, 108, 0.85)',
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 10,
          bgcolor: 'rgba(116, 114, 129, 0.91)',
        },
        borderRadius: '10px',
        color: 'rgba(255, 255, 255, 0.85)',
        cursor: 'pointer',
      }}
    >
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ mb: 2 }}>
          {item.tags && item.tags.length > 0 && (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
              {item.tags.slice(0, 3).map((tag, index) => (
                <Chip
                  key={index}
                  label={tag}
                  size="small"
                  color="default"
                  variant="outlined"
                  sx={{ 
                    fontSize: '0.7rem',
                    height: '20px',
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    color: 'rgba(255, 255, 255, 0.7)',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.5)',
                      color: 'rgba(255, 255, 255, 0.9)',
                    }
                  }}
                />
              ))}
              {item.tags.length > 3 && (
                <Chip
                  label={`+${item.tags.length - 3}`}
                  size="small"
                  color="default"
                  variant="outlined"
                  sx={{ 
                    fontSize: '0.7rem',
                    height: '20px',
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    color: 'rgba(255, 255, 255, 0.7)',
                  }}
                />
              )}
            </Box>
          )}
        </Box>
        
        <Typography 
          variant="h6" 
          component="h2" 
          gutterBottom
          sx={{ 
            fontWeight: 'bold',
            lineHeight: 1.3,
            mb: 2,
            flexGrow: 1,
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {item.title}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Edit sx={{ fontSize: 16, mr: 1, color: 'rgba(255, 255, 255, 0.7)' }} />
          <Typography variant="caption">
            {item.author}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccessTime sx={{ fontSize: 16, mr: 0.5 }} />
            <Typography variant="caption">
              {item.date}
            </Typography>
          </Box>
        </Box>
      </CardContent>
      
      <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
        <Button 
          size="small" 
          color="inherit" 
          onClick={(e) => {
            e.stopPropagation();
            onCardClick(item);
          }}
          sx={{ color: 'rgba(255, 255, 255, 0.85)' }}
        >
          Read More
        </Button>
        <Box>
          <IconButton 
            size="small" 
            onClick={(e) => {
              e.stopPropagation();
              handleShare(item.title);
            }}
            sx={{ mr: 1 }}
          >
            <Share fontSize="small" color="inherit" />
          </IconButton>
          <IconButton 
            size="small" 
            onClick={(e) => {
              e.stopPropagation();
              onInfoClick(item);
            }}
            color="inherit"
          >
            <Info fontSize="small" />
          </IconButton>
        </Box>
      </CardActions>
    </Card>
  );
};

export default NewsCard;
