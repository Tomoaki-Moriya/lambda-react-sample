FROM node:20.0.0 as builder

WORKDIR /app

COPY front .

RUN npm install && npm run build

FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}
COPY app.py requirements.txt ./
COPY --from=builder /app/dist ./dist

RUN pip install -r requirements.txt

CMD ["app.lambda_handler"]