const path = require('path');

const rootPath = path.join(__dirname, '../..');

const dllPath = path.join(__dirname, '../dll');

const srcPath = path.join(rootPath, 'src'); // our src path
const srcMainPath = path.join(srcPath, 'main'); // our electron app path
const srcRendererPath = path.join(srcPath, 'renderer'); // our react app path 

const releasePath = path.join(rootPath, 'release');
const appPath = path.join(releasePath, 'app'); // our release/app/ directory
const appPackagePath = path.join(appPath, 'package.json'); // the native modules package.json
const appNodeModulesPath = path.join(appPath, 'node_modules');
const srcNodeModulesPath = path.join(srcPath, 'node_modules');

const distPath = path.join(appPath, 'dist'); // distributable in the release path
const distMainPath = path.join(distPath, 'main'); // electron app in release/app/dist path  
const distRendererPath = path.join(distPath, 'renderer'); // react app in release/app/dist path 

const buildPath = path.join(releasePath, 'build');

export default {
  rootPath,
  dllPath,
  srcPath,
  srcMainPath,
  srcRendererPath,
  releasePath,
  appPath,
  appPackagePath,
  appNodeModulesPath,
  srcNodeModulesPath,
  distPath,
  distMainPath,
  distRendererPath,
  buildPath,
};
