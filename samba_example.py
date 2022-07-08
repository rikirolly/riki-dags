#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example use of SambaHook.
"""
import os
from os import path
from datetime import datetime
from airflow.providers.samba.hooks.samba import SambaHook


with DAG(
    "samba_example",
    schedule_interval='@daily',
    start_date=datetime(2021, 10, 1),
    tags=['riki'],
    catchup=False,
) as dag:


    def list_samba_folder(**kwargs):

        if path.exists('/home/kindshare'):
            print('RIKI - folder kindshare exist')
        else:
            print('RIKI - folder kindshare does not exist')

        try:
            samba = SambaHook(samba_conn_id='FileScanner')
            dir = samba.listdir()
            print(dir)
        except:
            logging.error("Error when creating samba connection: %s", sys.exc_info()[0])

    list_samba = PythonOperator(
        task_id='list_samba_folder_task',
        python_callable=list_samba_folder,
        dag=dag,
    )

    list_samba