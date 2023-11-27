import React, { useState } from 'react';
import { Button, Modal, Box } from '@mui/material';

import StripePricingTable from './StripePricingTable';
import './StripePricingTable.css';

function Upgrade() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const style = {
    position: 'absolute',
    top: '50%',
    borderRadius: '20px',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '80%',
    height: '90%',
    overflowY: 'scroll',
    bgcolor: '#387aff',
    boxShadow: 24,
    padding: '1em'
  };

  const handleClose = () => setIsModalOpen(false);

  return (
    <>
      <Button
        variant="contained"
        style={{
          color: 'white',
          borderRadius: '10px',
          background: 'black',
          border: 'solid 2px',
          marginRight: '.6em',
          paddingLeft: '2em',
          paddingRight: '2em'
        }}
        onClick={showModal}
      >
        Upgrade
      </Button>

      <Modal open={isModalOpen} onClose={handleClose}>
        <Box className="custom-scrollbar" sx={style}>
          <div style={{ height: '6em' }}></div>
          <StripePricingTable />
        </Box>
      </Modal>
    </>
  );
}

export default Upgrade;
