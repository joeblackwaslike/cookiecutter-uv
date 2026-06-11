import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "{{cookiecutter.project_name}}",
  tagline: "{{cookiecutter.description}}",
  favicon: "img/logo.svg",

  url: "https://{{cookiecutter.github_handle}}.github.io",
  baseUrl: "/{{cookiecutter.project_name}}/",
  organizationName: "{{cookiecutter.github_handle}}",
  projectName: "{{cookiecutter.project_name}}",
  trailingSlash: false,

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  plugins: [
    [
      "docusaurus-plugin-llms",
      {
        generateLLMsTxt: true,
        generateMarkdownFiles: true,
      },
    ],
  ],

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl:
            "https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/edit/main/docs/",
          routeBasePath: "/",
        },
        blog: false,
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    navbar: {
      title: "{{cookiecutter.project_name}}",
      items: [
        {
          type: "docSidebar",
          sidebarId: "mainSidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: "https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      copyright: `Copyright © ${new Date().getFullYear()} {{cookiecutter.author}}. Built with <a href="https://docusaurus.io">Docusaurus</a>.`,
    },
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
