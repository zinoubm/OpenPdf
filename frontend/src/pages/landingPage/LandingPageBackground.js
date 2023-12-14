import background from 'assets/images/hallow.png';
import './landingPage.css';

const LandingPageBackground = () => {
  return (
    <div
      style={{
        width: '100vw',
        position: 'absolute',
        overflow: 'hidden',
        zIndex: -1
      }}
    >
      <img src={background} className="hero-background" alt="openpdf-background" />
    </div>
  );
};

export default LandingPageBackground;
