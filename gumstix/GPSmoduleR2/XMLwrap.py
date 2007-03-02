def Row(string):
	return "\t<row>\n\t"+string+"\n\t</row>"

def Table(string):
	return "<table>\n"+string+"\n</table>"

def Field(Name_Value):
	data = ''
	for items in Name_Value:
		data = data+ "<field name =\"%s\">%s</field>"%(items[0],items[1]) 
	return data

def Wrap(Name_Value):
	data = ''
	data = Field(Name_Value)
	data = Row(data)
	data = Table(data)
	return data
	
