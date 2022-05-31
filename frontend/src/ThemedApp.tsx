import React from "react"
import { BaseProvider } from "baseui"
import { Global, useTheme } from "@emotion/react"

import ThemeProvider from "src/components/core/ThemeProvider"
import {
  AUTO_THEME_NAME,
  createAutoTheme,
  createPresetThemes,
  getDefaultTheme,
  globalStyles,
  isPresetTheme,
  removeCachedTheme,
  setCachedTheme,
  ThemeConfig,
  Theme,
} from "src/theme"

import AppWithScreencast from "./App"

function DataFrameOverlay(): React.ReactElement {
  const theme: Theme = useTheme()

  // The glide-data-grid requires one root level portal element for rendering the cell overlays:
  // https://github.com/glideapps/glide-data-grid/blob/main/packages/core/API.md#htmlcss-prerequisites
  // This is added to the body in ThemedApp

  return (
    <div
      id="portal"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: theme.zIndices.tablePortal,
        lineHeight: "100%",
      }}
    />
  )
}

const ThemedApp = (): JSX.Element => {
  const defaultTheme = getDefaultTheme()

  const [theme, setTheme] = React.useState<ThemeConfig>(defaultTheme)
  const [availableThemes, setAvailableThemes] = React.useState<ThemeConfig[]>([
    ...createPresetThemes(),
    ...(isPresetTheme(defaultTheme) ? [] : [defaultTheme]),
  ])

  const addThemes = (themeConfigs: ThemeConfig[]): void => {
    setAvailableThemes([...createPresetThemes(), ...themeConfigs])
  }

  const updateTheme = (newTheme: ThemeConfig): void => {
    if (newTheme !== theme) {
      setTheme(newTheme)

      // Only save to localStorage if it is not Auto since auto is the default.
      // Important to not save since it can change depending on time of day.
      if (newTheme.name === AUTO_THEME_NAME) {
        removeCachedTheme()
      } else {
        setCachedTheme(newTheme)
      }
    }
  }

  const updateAutoTheme = (): void => {
    if (theme.name === AUTO_THEME_NAME) {
      updateTheme(createAutoTheme())
    }
    const constantThemes = availableThemes.filter(
      theme => theme.name !== AUTO_THEME_NAME
    )
    setAvailableThemes([createAutoTheme(), ...constantThemes])
  }

  React.useEffect(() => {
    const mediaMatch = window.matchMedia("(prefers-color-scheme: dark)")
    mediaMatch.addEventListener("change", updateAutoTheme)

    return () => mediaMatch.removeEventListener("change", updateAutoTheme)
  }, [theme, availableThemes])

  return (
    <BaseProvider
      theme={theme.baseweb}
      zIndex={theme.emotion.zIndices.popupMenu}
    >
      <ThemeProvider theme={theme.emotion} baseuiTheme={theme.basewebTheme}>
        <Global styles={globalStyles} />
        <AppWithScreencast
          theme={{
            setTheme: updateTheme,
            activeTheme: theme,
            addThemes,
            availableThemes,
          }}
        />
        <DataFrameOverlay />
      </ThemeProvider>
    </BaseProvider>
  )
}

export default ThemedApp
