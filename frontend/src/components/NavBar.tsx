'use client'
import * as React from 'react';
import { useRouter } from 'next/navigation';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import ToggleButton from '@mui/material/ToggleButton';
import MenuItem from '@mui/material/MenuItem';

import { useParticles } from '@/contexts/ParticleContext';
import { AutoAwesome, Portrait } from '@mui/icons-material';

const pages = [
  { name: 'Home', path: '/' },
  { name: 'About', path: '/about' },
  { name: 'News Aggregator', path: '/news' }
];

function NavBar() {
  const router = useRouter();
  const [mounted, setMounted] = React.useState(false);
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const { particlesEnabled, toggleParticles } = useParticles();

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleNavigation = (path: string) => {
    router.push(path);
    setAnchorElNav(null);
  };

  return (
    <AppBar position="fixed" sx={{ 
      zIndex: 1000,
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
      margin: '16px',
      borderRadius: '12px',
      width: 'calc(100% - 32px)',
      backgroundColor: 'rgb(99, 99, 114)' // Black background
    }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', width: '100%' }}>
          {/* Left: Logo and Particles Toggle */}
          <Box sx={{ display: 'flex', alignItems: 'center', flexShrink: 0 }}>
            <Portrait sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
            <Typography
              variant="h6"
              noWrap
              component="a"
              href="/"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontFamily: 'monospace',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              PORTFOLIO
            </Typography>
            <ToggleButton
              value="particles"
              selected={particlesEnabled}
              onChange={toggleParticles}
              sx={{
                color: particlesEnabled ? 'white' : 'rgba(255,255,255,0.5)',
                borderColor: 'rgba(255,255,255,0.2)',
                bgcolor: particlesEnabled ? 'rgba(255,255,255,0.08)' : 'transparent',
                '&:hover': {
                  bgcolor: particlesEnabled ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.05)',
                },
                px: 1.5,
                py: 0.5,
                borderRadius: 2,
                ml: 1,
              }}
            >
              <AutoAwesome sx={{ fontSize: 22 }} />
            </ToggleButton>
          </Box>

          {/* Center: (empty, can be used for spacing) */}
          <Box sx={{ flexGrow: 1 }} />

          {/* Right: Navigation options */}
          <Box sx={{ flexGrow: 0, display: { xs: 'none', md: 'flex' }, alignItems: 'center', justifyContent: 'flex-end' }}>
            {pages.map((page) => (
              <Button
                key={page.name}
                onClick={() => handleNavigation(page.path)}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page.name}
              </Button>
            ))}
          </Box>

          {/* Mobile: Hamburger and mobile nav (unchanged) */}
          <Box sx={{ flexGrow: 0, display: { xs: 'flex', md: 'none' }, alignItems: 'center' }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: 'block', md: 'none' } }}
            >
              {pages.map((page) => (
                <MenuItem key={page.name} onClick={() => handleNavigation(page.path)}>
                  <Typography sx={{ textAlign: 'center' }}>{page.name}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default NavBar;