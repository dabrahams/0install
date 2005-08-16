import gtk, gobject

from dialog import Dialog

class CheckingBox(Dialog):
	show_details = False

	def __init__(self, root):
		Dialog.__init__(self)
		self.prog_name = root.get_name()
		self.set_title("Checking for updates")
		self.label = gtk.Label("Checking for updates to '%s'..." % self.prog_name)
		self.label.set_padding(10, 10)
		self.vbox.pack_start(self.label, True, True, 0)
		self.vbox.show_all()

		self.progress = gtk.ProgressBar()
		self.vbox.pack_start(self.progress, False, True, 0)
		self.progress.show()

		self.add_mixed_button('Details...', gtk.STOCK_ZOOM_IN, gtk.RESPONSE_OK)
		def response(w, r):
			if r == gtk.RESPONSE_OK:
				self.show_details = True
			self.destroy()
		self.connect('response', response)
	
	def updates_done(self, changes):
		"""Close the dialog after a short delay"""
		if changes:
			self.label.set_text("Updates found for '%s'" % self.prog_name)
		else:
			self.label.set_text("No updates for '%s'" % self.prog_name)
		self.progress.set_fraction(1)
		self.set_response_sensitive(gtk.RESPONSE_OK, False)
		gobject.timeout_add(1000, self.destroy)