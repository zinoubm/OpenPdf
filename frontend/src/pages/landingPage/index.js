import React from 'react';
import { Box } from '@mui/material';
import { Layout, Button, Typography } from 'antd';
import LandingPageBackground from 'pages/landingPage/LandingPageBackground';
import Logo from 'assets/images/openpdfLogo.svg';

const { Header } = Layout;

import './landingPage.css';

function LandingPage() {
  return (
    <Box>
      <LandingPageBackground />
      <Layout className="hero-layout" style={{ backgroundColor: 'transparent' }}>
        <Header className="hero-header">
          <img className="hero-logo" src={Logo} alt="OpenPdf" />
          <div className="hero-buttons-container">
            <Button className="hero-about-button" type="text" href="#">
              About
            </Button>
            <Button className="hero-cta-button" href="/login">
              Get Started
            </Button>
          </div>
        </Header>
        <div className="hero-container">
          <div className="typography-container">
            <Typography style={{ fontFamily: 'DM Serif Display, serif', fontSize: '4em', width: '75%' }}>
              Chat With Your Documents! No Hustle.
            </Typography>
            <Typography>Use AI and ask questions from your PDFs.</Typography>
            <Button href="/login" className="hero-cta-button">
              Get Started For Free
            </Button>
            <Button href="#" style={{ backgroundColor: 'transparent', border: 'solid 1px black', marginTop: '1em' }}>
              Join Our Group Chat
            </Button>
          </div>
        </div>
      </Layout>
    </Box>
  );
}

export default LandingPage;
