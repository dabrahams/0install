import os
from xml.dom import minidom, XMLNS_NAMESPACE

import basedir

from model import *

from namespaces import config_site, config_prog, XMLNS_IFACE

def add_text(parent, name, text):
	doc = parent.ownerDocument
	element = doc.createElementNS(XMLNS_IFACE, name)
	parent.appendChild(element)
	element.appendChild(doc.createTextNode(text))

def add_impl(parent, impl):
	if impl.user_stability:
		doc = parent.ownerDocument
		node = doc.createElementNS(XMLNS_IFACE, 'implementation')
		parent.appendChild(node)
		node.setAttribute('user-stability', str(impl.user_stability))
		node.setAttribute('id', impl.id)

def save_interface(interface):
	path = basedir.save_config_path(config_site, config_prog, 'user_overrides')
	path = os.path.join(path, escape(interface.uri))
	#print "Save to", path

	impl = minidom.getDOMImplementation()
	doc = impl.createDocument(XMLNS_IFACE, 'interface-preferences', None)

	root = doc.documentElement
	root.setAttributeNS(XMLNS_NAMESPACE, 'xmlns', XMLNS_IFACE)
	root.setAttribute('uri', interface.uri)

	if interface.stability_policy:
		root.setAttribute('stability-policy', str(interface.stability_policy))

	if interface.local_command:
		root.setAttribute('local-command', interface.local_command)

	if interface.last_checked:
		root.setAttribute('last-checked', str(interface.last_checked))

	impls = interface.implementations.values()
	impls.sort()
	for impl in impls:
		add_impl(root, impl)
	
	for feed in interface.feeds:
		elem = doc.createElementNS(XMLNS_IFACE, 'feed')
		root.appendChild(elem)
		elem.setAttribute('src', feed)

	doc.writexml(file(path + '.new', 'w'), addindent = " ", newl = '\n')
	os.rename(path + '.new', path)
