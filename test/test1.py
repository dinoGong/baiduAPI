import click
@click.command()
@click.option("-u",help="username")
@click.option("-p",help="password")
def fun(u,p):
  print("name:%s pass:%s" % (u,p))
if __name__=="__main__":
  fun()
