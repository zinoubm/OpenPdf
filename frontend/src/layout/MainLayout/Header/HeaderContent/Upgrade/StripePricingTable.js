import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';

const StripePricingTable = () => {
  const { userId, userEmail } = useSelector((state) => state.auth);
  const REACT_APP_STRIPE_PUBLISHABLE_KEY = process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY;
  const REACT_APP_STRIPE_PRICING_TABLE_ID = process.env.REACT_APP_STRIPE_PRICING_TABLE_ID;

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://js.stripe.com/v3/pricing-table.js';
    script.async = true;
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return React.createElement('stripe-pricing-table', {
    'pricing-table-id': REACT_APP_STRIPE_PRICING_TABLE_ID,
    'publishable-key': REACT_APP_STRIPE_PUBLISHABLE_KEY,
    'client-reference-id': userId,
    'customer-email': userEmail
  });
};
export default StripePricingTable;
