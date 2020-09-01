# Android Boot Animation Tools

### Simple command line utility for working with Android Boot Animations
  
This utility is made to simplify the process of creating Android-ready bootanimation.zip files

To install:  
  
Clone this git repository, and from the top-level directory (where setup.py is):

	pip3 install .

Alternatively, you can get the package from PyPi using:

	pip3 install abatools

Once installed, the abatools utility should be available from the command line.  Example:

	abatools -a bootanimation.zip

Help is available from the command line with the -h or --help option, but basic usage is as follows:  
  
  -a [filename.zip]     zip all files/folders in current directory to target [filename.zip]<br>
  -g [[gif file] [filename] [[gif file] [filename.zip]]]<br>
                        creates a boot animation from a target .gif and saves it to [filename.zip]

Questions or comments can be directed to threadreaper@gmail.com.  Pull requests are welcome if you discover any issues.

	Copyright [2020] [Michael Podrybau]

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or 
	implied.  See the License for the specific language governing 
	permissions and limitations under the License.