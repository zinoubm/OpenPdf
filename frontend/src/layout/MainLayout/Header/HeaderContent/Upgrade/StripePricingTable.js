import React, { useEffect } from 'react';

const StripePricingTable = () => {
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
    'pricing-table-id': 'prctbl_1OGIMSDjVJY9OEHxM4wy9x8K',
    'publishable-key': 'pk_test_51O7Jq2DjVJY9OEHxjqzH3YyvNSKc6Pys7bdPRUF3ivQpnTRz66NhXploW9FuCosL0Qal9aEH02hyfaJZP69thofb00TvRVHmyG'
  });
};
export default StripePricingTable;
