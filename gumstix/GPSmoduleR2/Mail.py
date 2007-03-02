import XMLwrap
import SlogModule

Data = (('Altitude','10'),('Latitude','100'))

Table = XMLwrap.Wrap(Data)
Entry=('kimyh@ucla.edu','password','85','Mtest')

SlogModule.DataSlog().WrapSlog((Entry,Table))
