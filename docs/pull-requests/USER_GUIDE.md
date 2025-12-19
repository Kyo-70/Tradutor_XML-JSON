# Visual User Guide - What Changed

## 1. Auto-Adjust on Edit Start

### Before:
```
User double-clicks to edit → Row stays small/compressed → Hard to see long text
```

### After:
```
User double-clicks to edit → Row immediately expands → Full text visible
```

**What the user sees:**
- When you double-click a cell to edit it, the row automatically expands
- Long translations that were cut off are now fully visible
- Makes editing much more comfortable

**Where**: Main translation table and database viewer

---

## 2. API Status Display

### New Section in Settings Dialog:

```
┌─────────────────────────────────────────┐
│ 📋 Status das APIs Configuradas         │
├─────────────────────────────────────────┤
│ DeepL: ✅ Configurada                   │
│ Google: ⏳ Não configurada              │
│ MyMemory: ⏳ Não configurada            │
│ LibreTranslate: ✅ Configurada         │
└─────────────────────────────────────────┘
```

**What the user sees:**
- Clear visual indicator showing which APIs are set up
- ✅ means the API is ready to use
- ⏳ means you need to configure it
- Updates automatically when you add/save an API

**Where**: Settings dialog (⚙️ Config button) → APIs de Tradução tab

---

## 3. DEL Key to Clear Translations

### Workflow:

1. **Select row(s)** in the translation table
2. **Press DEL key**
3. **Confirm** in dialog:
   ```
   ┌─────────────────────────────────────┐
   │ Confirmar Limpeza                   │
   ├─────────────────────────────────────┤
   │ Limpar tradução de 3 linha(s)      │
   │ selecionada(s)?                     │
   │                                     │
   │           [Sim]    [Não]            │
   └─────────────────────────────────────┘
   ```
4. **Result**: Translation text cleared, status changes to ⏳

### Before:
```
Row: "Hello" → "Olá" [✅]
(No quick way to clear the translation)
```

### After pressing DEL:
```
Row: "Hello" → "" [⏳]
(Translation cleared, ready for new translation)
```

**What the user sees:**
- Select one or more rows
- Press DEL key
- Confirm the action
- Translation text is cleared (original text remains)
- Status icon changes from ✅ to ⏳
- Row color changes back to default

**Where**: Main translation table (the big table in the center)

---

## Summary of Keyboard Shortcuts

| Key | Action | Location |
|-----|--------|----------|
| **Double-Click** | Edit cell + auto-adjust height | Main table, Database viewer |
| **DEL** | Clear translation from selected rows | Main table |
| **Ctrl+C** | Copy selected rows | Main table |
| **Ctrl+V** | Paste translations | Main table |

---

## Visual Examples

### Auto-Adjust Example:

**Before double-click:**
```
┌───┬───────────────────┬──────────────────┬────┐
│ # │ Original          │ Translation      │ St │
├───┼───────────────────┼──────────────────┼────┤
│ 1 │ This is a very... │ Esta é uma tra...│ ⏳ │  ← Small row
└───┴───────────────────┴──────────────────┴────┘
```

**After double-click (auto-adjusts):**
```
┌───┬─────────────────────────────┬────────────────────────────┬────┐
│ # │ Original                    │ Translation                │ St │
├───┼─────────────────────────────┼────────────────────────────┼────┤
│ 1 │ This is a very long text    │ Esta é uma tradução muito  │ ⏳ │
│   │ that needs multiple lines   │ longa que precisa de       │    │  ← Expanded!
│   │ to display properly         │ várias linhas              │    │
└───┴─────────────────────────────┴────────────────────────────┴────┘
       ↑ NOW you can see and edit the full text
```

### Clear Translation Example:

**Before DEL (selected rows 1 and 3):**
```
┌───┬────────────┬──────────────┬────┐
│ # │ Original   │ Translation  │ St │
├───┼────────────┼──────────────┼────┤
│ 1 │ Hello      │ Olá          │ ✅ │ ← Selected
│ 2 │ World      │ Mundo        │ ✅ │
│ 3 │ Test       │ Teste        │ ✅ │ ← Selected
└───┴────────────┴──────────────┴────┘
```

**After DEL + Confirm:**
```
┌───┬────────────┬──────────────┬────┐
│ # │ Original   │ Translation  │ St │
├───┼────────────┼──────────────┼────┤
│ 1 │ Hello      │              │ ⏳ │ ← Cleared!
│ 2 │ World      │ Mundo        │ ✅ │ ← Not selected, unchanged
│ 3 │ Test       │              │ ⏳ │ ← Cleared!
└───┴────────────┴──────────────┴────┘
```

---

## Benefits for Users

1. **Faster Editing**: No need to manually expand rows - happens automatically
2. **Better Visibility**: Always see the full text when editing
3. **Easy Correction**: Quick way to clear wrong translations with DEL key
4. **API Transparency**: Know at a glance which APIs are ready to use
5. **Improved Workflow**: Less clicks, more productivity

---

## No Breaking Changes

✅ All existing features work exactly as before
✅ All shortcuts still work (Ctrl+C, Ctrl+V, F5, etc.)
✅ All buttons and menus work the same
✅ Your translations and database are safe

**These are pure improvements - nothing breaks!**
