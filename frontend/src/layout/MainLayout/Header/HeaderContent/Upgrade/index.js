import React, { useState, useEffect } from 'react';
import { Button, Modal, Box } from '@mui/material';
import useApi from 'api/hooks/useApi';
import { useSelector, useDispatch } from 'react-redux';
import { activePaymentSummary } from 'store/reducers/app';

import { Popover } from 'antd';

import StripePricingTable from './StripePricingTable';
import './StripePricingTable.css';

function Upgrade() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { getPaymentSummary, getCustomerPortalUrl } = useApi();
  const { paymentSummary } = useSelector((state) => state.app);

  const dispatch = useDispatch();

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
    bgcolor: '#f5f9ff',
    boxShadow: 24,
    padding: '1em'
  };

  const handleClose = () => setIsModalOpen(false);

  const handleGetRedirectUrl = async () => {
    const url = await getCustomerPortalUrl();
    window.location.href = url;
  };

  useEffect(() => {
    const getPaymentSummaryRequest = async (dispatch) => {
      const response = await getPaymentSummary();
      if (response.success) {
        dispatch(activePaymentSummary({ paymentSummary: response.data }));
      }
    };

    getPaymentSummaryRequest(dispatch);
  }, []);

  return (
    <>
      {!paymentSummary || paymentSummary.plan === 'FREE' ? (
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
      ) : (
        <Popover content={<div>Update your subscription plan.</div>} title="Manage">
          <Button
            variant="contained"
            style={{
              color: 'white',
              borderRadius: '10px',
              border: 'solid 2px',
              background: '#0ec295',
              marginRight: '.6em',
              paddingLeft: '2em',
              paddingRight: '2em'
            }}
            onClick={handleGetRedirectUrl}
          >
            Manage
          </Button>
        </Popover>
      )}

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
