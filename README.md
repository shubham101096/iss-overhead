# issoverhead
Project runs a script every minute to check if the ISS(international space station) is overhead wrt our longitude and latitude and if it is night time. If both conditions are true, it sends an email to us to look above to see ISS. 
It uses open notify API to check the current ISS location. 
It also checks whether the current time lies between sunset and sunrise using sunrise-sunset api.
