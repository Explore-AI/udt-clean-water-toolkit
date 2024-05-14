// https://medium.com/@dimi_2011/setting-up-css-modules-in-typescript-project-52596526d19
//https://stackoverflow.com/questions/41336858/how-to-import-css-modules-with-typescript-react-and-webpack
declare module '*.module.css';
// https://webpack.js.org/guides/typescript/#importing-other-assets
declare module '*.svg' {
    const content: any;
    export default content;
}
