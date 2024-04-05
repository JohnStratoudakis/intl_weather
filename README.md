# intl_weather
Weather Widget

https://www.weather.gov/documentation/services-web-api
=======
To package for AWS

```
pip3 install --target ./package requests
cd package
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_functions.py
```

Upload my_deployment_package

D
