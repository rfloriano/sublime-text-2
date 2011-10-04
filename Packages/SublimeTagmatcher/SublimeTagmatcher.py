import sublime, sublime_plugin, Elements

class SublimeTagmatcher(sublime_plugin.EventListener):

  # Customize
  #--------------------
  # Scope? (Defined in theme files.) ->
  # Examples: (keyword/string/number)
  Scope = 'entity.name.class'
  # Outline? (True/False) ->
  Outline = True
  # Icon? (dot/circle/bookmark/cross)
  Icon = 'dot'
  #--------------------
  # End Customize

  view = None
  window = None
  last_id_view = None
  last_id_sel = None
  highlight_us = None

  def on_selection_modified(self, view):
    self.view = view
    self.window = self.view.window()
    self.last_view = view

    if(self.unique()):
      # Clear views.
      self.highlight_us = []
      if self.window != None:
        for clear_view in self.window.views():
          self.highlight(clear_view)
      # Process selections.
      for sel in self.view.sel():
        self.highlight_tags(sel)
    # Highlight.
    self.highlight(view)

  def unique(self):
    id_view = self.view.id()
    id_sel = ''
    for sel in self.view.sel():
      id_sel = id_sel + str(sel.a)
    if( id_view != self.last_id_view or
        id_sel != self.last_id_sel):
      self.last_id_view = id_view
      self.last_id_sel = id_sel
      return True
    else:
      return False

  def highlight(self, view):

    # Curly Highlight.
    if(self.Outline == True):
      self.view.add_regions(
        'highlight', 
        self.highlight_us, 
        self.Scope,
        self.Icon,
        sublime.DRAW_OUTLINED
      )
    elif(self.Outline == False):
      self.view.add_regions(
        'highlight', 
        self.highlight_us, 
        self.Scope,
        self.Icon,
        sublime.HIDE_ON_MINIMAP
      )

  def highlight_tags(self, sel):

    # Make sure only clicking
    if(sel.empty() != True):
      blotch = True

    bufferSize = self.view.size()
    bufferRegion = sublime.Region(0, bufferSize)
    bufferText = self.view.substr(bufferRegion)
    curPosition = sel.begin()
    foundTags = Elements.match(bufferText, curPosition, 'html')
    tag1 = { "match": foundTags[0] }
    tag2 = { "match": foundTags[1] }
    if( str(tag1['match']) != 'None' and 
        self.view.substr(tag1['match'] + 1) != '!' and 
        self.view.substr(tag1['match'] - 1) != '`' and 
        self.view.substr(tag1['match']) == '<' and 
        self.view.substr(curPosition) != '<'):

      # Get 1st Tag
      blotch = False
      tag1['begin'] = tag1['match']
      tag1['end'] = tag1['match']
      while(self.view.substr(tag1['end']) != '>'):
        tag1['end'] = tag1['end'] + 1
        if(self.view.substr(tag1['end']) == '<'):
          blotch = True
      tag1['region'] = sublime.Region(tag1['begin'], tag1['end'] + 1)

      # Get 2nd Tag
      tag2['end'] = tag2['match'] - 1
      tag2['begin'] = tag2['end']
      while(self.view.substr(tag2['begin']) != '<'):
        tag2['begin'] = tag2['begin'] - 1
      tag2['region'] = sublime.Region(tag2['begin'], tag2['end'] + 1)

      # Highlight
      if(blotch == False):
        self.highlight_us.append(tag1['region'])
        self.highlight_us.append(tag2['region'])