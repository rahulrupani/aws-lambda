Getting started
===============

Lambda Notification package is implemented for deploying a lambda that you can invoke to execute cloud insight query and shared results via Email (Amazon SES).


Prerequisites
#############

Pre-Configured Amazon SES service 

You can use `Serverless framework <https://www.serverless.com/framework/docs/providers/aws/guide/installation/>`_ for deploying the lambda function:
if you want to use the guide below, you have to install Serverless framework before

.. code-block:: bash

    npm install
    npm install -g serverless
    

If you want to use another AWS tool, you can see the repository `aws-tool-comparison <https://github.com/bilardi/aws-tool-comparison>`_ before to implement your version.

Configuration
############

Find #*** in ;ambda-notification/lambda_function.py and serverless.yml and update your data.
or
We can say that all the feilda marked with #*** need to be updated. 


Installation
############

The package is not self-consistent. So you have to download the package by github and to install the requirements before to deploy on AWS:

.. code-block:: bash
    export AWS_PROFILE=your-account
    cd lambda-notification/lambda
    sls deploy 
