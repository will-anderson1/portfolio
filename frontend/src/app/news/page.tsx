'use client';

import React, { useEffect, useState } from 'react';
import {
  Container,
  Box,
  CircularProgress,
  Typography,
} from '@mui/material';
import NewsCard, { NewsItem } from './components/NewsCard';
import NewsDetailModal from './components/NewsDetailModal';
import { ApiClient, AggregateArticle } from '@/lib/NewsApi';

const NewsPage = () => {
  const [articles, setArticles] = useState<AggregateArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedArticle, setSelectedArticle] = useState<AggregateArticle | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const apiClient = new ApiClient();

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getNews();
        setArticles(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch articles');
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  const handleInfoClick = (item: NewsItem) => {
    // Find the original article
    const originalArticle = articles.find(article => article.title === item.title);
    if (originalArticle) {
      setSelectedArticle(originalArticle);
      setModalOpen(true);
    }
  };

  const handleCardClick = (item: NewsItem) => {
    // Find the original article
    const originalArticle = articles.find(article => article.title === item.title);
    if (originalArticle) {
      setSelectedArticle(originalArticle);
      setModalOpen(true);
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedArticle(null);
  };

  const convertToNewsItem = (article: AggregateArticle): NewsItem => {
    return {
      id: Math.random(),
      title: article.title,
      excerpt: article.description,
      image: article.imageUrl,
      author: article.sources[0]?.name || 'Unknown',
      date: new Date(article.latestUpdateDateTime).toLocaleDateString(),
      tags: article.tags.slice(1),
    };
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Typography variant="h6" color="error" align="center">
          Error: {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, 1fr)',
            md: 'repeat(3, 1fr)',
            lg: 'repeat(4, 1fr)',
          },
          gap: 3,
        }}
      >
        {articles.map((article) => (
          <NewsCard 
            key={article.title} 
            item={convertToNewsItem(article)} 
            onInfoClick={handleInfoClick}
            onCardClick={handleCardClick}
          />
        ))}
      </Box>
      
      <NewsDetailModal
        open={modalOpen}
        onClose={handleCloseModal}
        article={selectedArticle}
      />
    </Container>
  );
};

export default NewsPage;
