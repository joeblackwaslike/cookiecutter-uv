import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "{{cookiecutter.project_name}}",
  tagline: "{{cookiecutter.description}}",
  favicon: "img/favicon.ico",
  url: "https://{{cookiecutter.github_handle}}.github.io",
  baseUrl: "/{{cookiecutter.project_name}}/",
  organizationName: "{{cookiecutter.github_handle}}",
  projectName: "{{cookiecutter.project_name}}",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  i18n: { defaultLocale: "en", locales: ["en"] },
  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl:
            "https://github.com/{{cookiecutter.github_handle}}/{{cookiecutter.project_name}}/tree/main/docs/",
        },
        blog: false,
        theme: { customCss: "./src/css/custom.css" },
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    navbar: {
      title: "{{cookiecutter.project_name}}",
      items: [
        {
          type: "docSidebar",
          sidebarId: "docs",
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
      copyright: `Copyright © ${new Date().getFullYear()} {{cookiecutter.author}}. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ["python", "bash", "toml"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
