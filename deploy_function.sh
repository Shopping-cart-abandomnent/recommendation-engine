cp requirements.txt src/
cd src
gcloud functions deploy \
reco-product \
--entry-point receive_msg \
--trigger-topic Shopping_Cart_Abandonment \
--runtime python39 \
--memory=2048MB \
--set-env-vars SENDGRID_API_KEY=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
rm src/requirements.txt