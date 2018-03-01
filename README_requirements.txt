#Instalar requisitos utilizando
#pip install -r requirements.txt
#---
#Para Actualizar requisitos: pip freeze > requirements.txt
#--
#IMPORTANTE: Hay que instalar manualmente PhantomJS,
#Ya que hay partes del código en las que se
#utiliza PhantomJS con Selenium.
#----
#INTRUCIIONES PHATNOMJS
#LINK: https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python
#(3ra. respueta)
#
#Now since the GhostDriver comes bundled with the PhantomJS, it has become even more convenient to use it through Selenium.
#
#I tried the Node installation of PhantomJS, as suggested by Pykler, but in practice I found it to be slower than the standalone installation of PhantomJS. I guess standalone installation didn't provided these features earlier, but as of v1.9, it very much does so.
#
#    Install PhantomJS (http://phantomjs.org/download.html) (If you are on Linux, following instructions will help https://stackoverflow.com/a/14267295/382630)
#        Install Selenium using pip.
#
#        Now you can use like this
#
#        import selenium.webdriver
#        driver = selenium.webdriver.PhantomJS()
#        driver.get('http://google.com')
#        # do some processing
#
#        driver.quit()
#
#
#----
