-- disable payumoney payment provider
UPDATE payment_provider
   SET qnb_email = NULL,
       qnb_public_key = NULL,
       qnb_private_key = NULL;
