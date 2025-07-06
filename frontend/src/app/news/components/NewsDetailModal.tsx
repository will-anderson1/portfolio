'use client';

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Link,
  IconButton,
} from '@mui/material';
import {
  Close,
  AccessTime,
  Source,
  Update,
  Share,
  OpenInNew,
  Edit,
} from '@mui/icons-material';
import { AggregateArticle } from '@/lib/NewsApi';

interface NewsDetailModalProps {
  open: boolean;
  onClose: () => void;
  article: AggregateArticle | null;
}

const NewsDetailModal: React.FC<NewsDetailModalProps> = ({ open, onClose, article }) => {
  if (!article) return null;

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: article.title,
        text: article.description,
        url: article.url || window.location.href,
      });
    } else {
      navigator.clipboard.writeText(`${article.title}\n\n${article.description}\n\n${article.url || window.location.href}`);
      alert('Article information copied to clipboard!');
    }
  };

  const handleOpenUrl = () => {
    if (article.url) {
      window.open(article.url, '_blank');
    }
  };

  const formatDate = (dateInput: string | Date) => {
    const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput;
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          bgcolor: 'rgba(98, 96, 108, 0.95)',
          color: 'rgba(255, 255, 255, 0.9)',
          borderRadius: '12px',
          backdropFilter: 'blur(10px)',
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        pb: 1
      }}>
        <Typography variant="h5" component="span" sx={{ fontWeight: 'bold' }}>
          {article.title}
        </Typography>
        <IconButton onClick={onClose} sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
          <Close />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ pt: 0 }}>
        {/* Tags */}
        {article.tags && article.tags.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle2" sx={{ mb: 1, color: 'rgba(255, 255, 255, 0.8)' }}>
              Categories & Tags
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {article.tags.map((tag, index) => (
                <Chip
                  key={index}
                  label={tag}
                  size="small"
                  variant="outlined"
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    color: 'rgba(255, 255, 255, 0.8)',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.5)',
                    }
                  }}
                />
              ))}
            </Box>
          </Box>
        )}

        {/* Description */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
            {article.description}
          </Typography>
        </Box>

        <Divider sx={{ my: 2, borderColor: 'rgba(255, 255, 255, 0.2)' }} />

        {/* Sources */}
        {article.sources && article.sources.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
              <Source sx={{ mr: 1, fontSize: 20 }} />
              Sources
            </Typography>
            <List dense>
              {article.sources.map((source, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <Edit sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.7)' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Link
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.9)',
                          textDecoration: 'none',
                          '&:hover': { textDecoration: 'underline' }
                        }}
                      >
                        {source.name}
                      </Link>
                    }
                    secondary={
                      <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                        {source.citation}
                      </Typography>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        )}

        {/* Update History */}
        {article.updateHistory && article.updateHistory.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
              <Update sx={{ mr: 1, fontSize: 20 }} />
              Update Log
            </Typography>
            <Box sx={{ 
              bgcolor: 'rgba(0, 0, 0, 0.2)', 
              borderRadius: '8px', 
              p: 2,
              maxHeight: '300px',
              overflowY: 'auto'
            }}>
              {[...article.updateHistory]
                .sort((a, b) => new Date(b.dateTime).getTime() - new Date(a.dateTime).getTime())
                .map((update, index) => (
                <Box 
                  key={index} 
                  sx={{ 
                    mb: index < article.updateHistory.length - 1 ? 2 : 0,
                    pb: index < article.updateHistory.length - 1 ? 2 : 0,
                    borderBottom: index < article.updateHistory.length - 1 ? '1px solid rgba(255, 255, 255, 0.1)' : 'none'
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <AccessTime sx={{ 
                      fontSize: 16, 
                      color: 'rgba(255, 255, 255, 0.6)',
                      mt: 0.2
                    }} />
                    <Box sx={{ flex: 1 }}>
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.9)',
                          fontWeight: 500,
                          mb: 0.5
                        }}
                      >
                        {update.description}
                      </Typography>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.5)',
                          fontFamily: 'monospace'
                        }}
                      >
                        {formatDate(update.dateTime)}
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              ))}
            </Box>
          </Box>
        )}

        {/* Metadata */}
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          p: 2,
          bgcolor: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '8px'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccessTime sx={{ fontSize: 16, mr: 1, color: 'rgba(255, 255, 255, 0.7)' }} />
            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
              Last Updated: {formatDate(article.latestUpdateDateTime)}
            </Typography>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 3, gap: 1 }}>
        <Button
          onClick={handleShare}
          startIcon={<Share />}
          sx={{ 
            color: 'rgba(255, 255, 255, 0.8)',
            borderColor: 'rgba(255, 255, 255, 0.3)',
            '&:hover': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
              bgcolor: 'rgba(255, 255, 255, 0.1)',
            }
          }}
          variant="outlined"
        >
          Share
        </Button>
        
        {article.url && (
          <Button
            onClick={handleOpenUrl}
            startIcon={<OpenInNew />}
            sx={{ 
              color: 'rgba(255, 255, 255, 0.8)',
              borderColor: 'rgba(255, 255, 255, 0.3)',
              '&:hover': {
                borderColor: 'rgba(255, 255, 255, 0.5)',
                bgcolor: 'rgba(255, 255, 255, 0.1)',
              }
            }}
            variant="outlined"
          >
            Open Article
          </Button>
        )}
        
        <Button
          onClick={onClose}
          sx={{ 
            color: 'rgba(255, 255, 255, 0.8)',
            bgcolor: 'rgba(255, 255, 255, 0.1)',
            '&:hover': {
              bgcolor: 'rgba(255, 255, 255, 0.2)',
            }
          }}
        >
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewsDetailModal; 