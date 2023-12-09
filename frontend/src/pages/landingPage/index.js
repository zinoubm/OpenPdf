import React from 'react';
import { Button, Typography } from 'antd';
// import { Button } from 'antd';

import LandingPageBackground from 'pages/landingPage/LandingPageBackground';
import Logo from 'assets/images/openpdfLogo.svg';
import MessageFeature from 'assets/images/message-feature.png';
import UploadFeature from 'assets/images/upload-feature.png';

import SuggestionsFeature from 'assets/images/suggestions-feature.png';
import featuresPreview from 'assets/images/features-preview.png';

// const { Header } = Layout;

import './landingPage.css';

function LandingPage() {
  return (
    <>
      <LandingPageBackground />
      <header className="hero-header">
        <div className="branding">
          <img className="hero-logo" src={Logo} alt="OpenPdf" />
        </div>
        <div className="hero-header-buttons-container">
          <Button className="hero-about-button" size="large" type="text" href="#">
            About
          </Button>
          <Button className="hero-cta-button" size="large" href="/login">
            Get Started
          </Button>
        </div>
      </header>
      <section className="hero-section section">
        <div className="hero-typography-container">
          <Typography className="hero-typography-header" style={{ fontFamily: 'DM Serif Display, serif' }}>
            Chat with Documents.
            <br />
            Read 64% Faster!
          </Typography>
          <Typography className="hero-typography-description">No Time? Get your answers in 1 click! </Typography>
          <Button href="/login" className="hero-cta-button" size="large">
            Get Started For Free
          </Button>
        </div>
        <div>
          <img className="hero-image" src={featuresPreview} alt="features" />
        </div>
      </section>

      {/* features */}
      <div className="typography-section section">
        <div className="typography-section-text">
          <Typography className="typography-section-text-header" style={{ fontFamily: 'DM Serif Display, serif' }}>
            Tired of Scouring Through Lengthy PDFs?
          </Typography>
          <Typography className="typography-section-text-description">
            Are you tired of spending hours sifting through dense PDF documents, searching for that elusive piece of information? Say hello
            to a groundbreaking solution that transforms your document interaction experience.{' '}
          </Typography>
        </div>
        <div className="typography-section-image">
          <img className="typography-section-image-image" src={MessageFeature} alt="message-feature"></img>
        </div>
      </div>

      <div className="typography-section section">
        <div className="typography-section-image">
          <img className="typography-section-image-image" src={SuggestionsFeature} alt="message-feature"></img>
        </div>
        <div className="typography-section-text">
          <Typography className="typography-section-text-header" style={{ fontFamily: 'DM Serif Display, serif' }}>
            Revolutionary Chat-Based Document Interaction!
          </Typography>
          <Typography className="typography-section-text-description">
            Our app revolutionizes the way you engage with your PDFs. No longer do you have to navigate lengthy pages or get lost in a sea
            of text. With our innovative chat-based approach, you can now converse directly within your documents.{' '}
          </Typography>
        </div>
      </div>

      <Typography className="hero-typography-header" style={{ fontFamily: 'DM Serif Display, serif', textAlign: 'center' }}>
        Key Features
      </Typography>

      <div className="features-cards-section">
        <div className="feature-card">
          <div className="feature-card-typography">
            <Typography style={{ fontSize: '2.4em', fontFamily: 'DM Serif Display, serif', textAlign: 'center' }}>
              Uplaod Your PDF,
            </Typography>
            <Typography className="feature-card-typography-description">
              Click the upload button from your OpenPDFaI dashboard and choose a PDF document and hit Enter.
            </Typography>
          </div>
          <div className="center">
            <img style={{ width: '54%' }} src={UploadFeature} alt="message-feature"></img>
          </div>
        </div>

        <div className="feature-card">
          <div className="feature-card-typography">
            <Typography style={{ fontSize: '2.4em', fontFamily: 'DM Serif Display, serif', textAlign: 'center' }}>
              Start Chatting!
            </Typography>
            <Typography className="feature-card-typography-description">
              Select a document form the left hand side menu and enter your question and send It!{' '}
            </Typography>
          </div>
          <div className="center">
            <img style={{ width: '100%' }} src={MessageFeature} alt="message-feature"></img>
          </div>
        </div>
      </div>

      <Typography className="hero-typography-header" style={{ fontFamily: 'DM Serif Display, serif', textAlign: 'center' }}>
        Can{"'"}t be Simpler!
      </Typography>

      <div className="center">
        <Button className="hero-cta-button" size="large" href="/login">
          Get Started
        </Button>
        <img className="hero-logo" src={Logo} alt="OpenPdf" style={{ margin: '2em' }} />
      </div>

      {/*       <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography
          className="typography-header"
          style={{ fontFamily: 'DM Serif Display, serif', margin: 'auto', textAlign: 'center', width: '40%' }}
        >
          Can{"'"}t Be Simpler
        </Typography>

        <div>
          <Button className="hero-cta-button" size="large" href="/login">
            Get Started
          </Button>
        </div>
        <img className="hero-logo" src={Logo} alt="OpenPdf" style={{ margin: '2em' }} />
      </div> */}
    </>
  );
}

export default LandingPage;
