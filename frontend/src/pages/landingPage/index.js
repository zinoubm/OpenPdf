import React from 'react';
import { Box } from '@mui/material';
import { Layout, Button, Typography } from 'antd';
import LandingPageBackground from 'assets/images/landingPage/LandingPageBackground';
import Logo from 'assets/images/openpdfLogo.svg';

const { Header } = Layout;

import './style.css';

function LandingPage() {
  return (
    <Box>
      <LandingPageBackground />
      <Layout className="hero-layout" style={{ backgroundColor: 'transparent' }}>
        <Header
          className="hero-header"
          style={{ height: '12vh', backgroundColor: 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
        >
          <img className="hero-logo" src={Logo} style={{ width: '10em' }} alt="OpenPdf" />
          <div className="hero-buttons-container" style={{ width: '20%' }}>
            <Button className="hero-about-button" style={{ marginRight: '1em' }} type="text" href="#">
              About
            </Button>
            <Button className="hero-cta-button" href="/login" style={{ backgroundColor: 'transparent', border: 'solid 1px black' }}>
              Get Started
            </Button>
          </div>
        </Header>
        <div style={{ display: 'flex' }}>
          <div style={{ width: '50%', height: '100vh', padding: '4em' }}>
            <Typography style={{ fontFamily: 'DM Serif Display, serif', fontSize: '4em', width: '75%' }}>
              Chat With Your Documents! No Hustle.
            </Typography>
            <Typography>Use AI and ask questions from your PDFs.</Typography>
            <Button
              href="/login"
              style={{ backgroundColor: 'transparent', border: 'solid 1px black', marginTop: '1em', marginRight: '.6em' }}
            >
              Get Started For Free
            </Button>
            <Button href="#" style={{ backgroundColor: 'transparent', border: 'solid 1px black', marginTop: '1em' }}>
              Join Our Group Chat
            </Button>
          </div>
          <div style={{ width: '50%', height: '100vh' }}>-</div>
        </div>
      </Layout>
    </Box>
  );
}

export default LandingPage;
