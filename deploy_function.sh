cp requirements.txt src/
cd src
gcloud functions deploy \
reco-product \
--entry-point receive_msg \
--trigger-topic Shopping_Cart_Abandonment \
--runtime python39 \
--memory=2048MB \
--set-env-vars SENDGRID_API_KEY=$1
rm requirements.txt