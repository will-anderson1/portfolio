import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Avatar, Box, Divider, List, ListItem, ListItemIcon } from '@mui/material';
import React from 'react';
import SchoolIcon from '@mui/icons-material/School';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import GradeIcon from '@mui/icons-material/Grade';

interface InfoModalProps {
  open: boolean;
  onClose: () => void;
  modalData: any;
  modalType: 'education' | 'work' | null;
}

const InfoModal: React.FC<InfoModalProps> = ({ open, onClose, modalData, modalType }) => (
  <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
    <DialogTitle sx={{ bgcolor: 'rgba(98, 96, 108, 0.95)', color: 'rgba(255,255,255,0.95)', display: 'flex', alignItems: 'center', gap: 2 }}>
      {modalData?.logo && (
        modalData.logo.endsWith('.svg') ? (
          <img
            src={modalData.logo}
            alt={modalType === 'education' ? modalData.school : modalData.company}
            style={{ height: 40, width: 'auto', marginRight: 16, display: 'block', maxWidth: 80, background: 'transparent' }}
          />
        ) : (
          <Avatar src={modalData.logo} alt={modalType === 'education' ? modalData.school : modalData.company} sx={{ width: 40, height: 40, mr: 2 }} />
        )
      )}
      <Box>
        <Typography variant="h6" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          {modalType === 'education' ? <SchoolIcon sx={{ fontSize: 24, mr: 1 }} /> : <BusinessCenterIcon sx={{ fontSize: 24, mr: 1 }} />}
          {modalType === 'education' ? modalData?.degree : modalData?.position}
        </Typography>
        <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.7)', display: 'flex', alignItems: 'center', gap: 1 }}>
          <CalendarMonthIcon sx={{ fontSize: 18, mr: 0.5 }} />
          {modalType === 'education'
            ? `${modalData?.school} · ${modalData?.years}`
            : `${modalData?.company} · ${modalData?.years}`}
        </Typography>
      </Box>
    </DialogTitle>
    <DialogContent sx={{ bgcolor: 'rgba(98, 96, 108, 0.95)', color: 'rgba(255,255,255,0.9)' }}>
      {modalType === 'education' && modalData && (
        <>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
            <GradeIcon sx={{ fontSize: 20, color: 'gold', mr: 1 }} />
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              GPA: {modalData.gpa}
            </Typography>
          </Box>
          <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.15)' }} />
          <Typography variant="subtitle2" sx={{ mb: 1, color: 'rgba(255,255,255,0.8)' }}>
            Highlights
          </Typography>
          <List dense>
            {modalData.details.map((detail: string, i: number) => (
              <ListItem key={i} sx={{ pl: 0 }}>
                <ListItemIcon sx={{ minWidth: 32, color: 'rgba(255,255,255,0.7)' }}>
                  <SchoolIcon fontSize="small" />
                </ListItemIcon>
                <Typography variant="body2">{detail}</Typography>
              </ListItem>
            ))}
          </List>
        </>
      )}
      {modalType === 'work' && modalData && (
        <>
          <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.15)' }} />
          <Typography variant="subtitle2" sx={{ mb: 1, color: 'rgba(255,255,255,0.8)' }}>
            Responsibilities & Achievements
          </Typography>
          <List dense>
            {modalData.details.map((detail: string, i: number) => (
              <ListItem key={i} sx={{ pl: 0 }}>
                <ListItemIcon sx={{ minWidth: 32, color: 'rgba(255,255,255,0.7)' }}>
                  <BusinessCenterIcon fontSize="small" />
                </ListItemIcon>
                <Typography variant="body2">{detail}</Typography>
              </ListItem>
            ))}
          </List>
        </>
      )}
    </DialogContent>
    <DialogActions sx={{ bgcolor: 'rgba(98, 96, 108, 0.95)' }}>
      <Button onClick={onClose} sx={{ color: 'rgba(255,255,255,0.85)' }}>Close</Button>
    </DialogActions>
  </Dialog>
);

export default InfoModal; 