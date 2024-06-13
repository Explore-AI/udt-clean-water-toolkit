export const splitAssetName = (name: string) => {
    return name.replace(/_/g, ' ');
};

export const getDmas = (dmaString: string) => {
    if (!dmaString || dmaString == '') return { codes: ['NA'], names: ['NA'] };
    const dmas = JSON.parse(dmaString);
    const codes = dmas.map((dma: { code: string; name: string }) => dma.code);
    const names = dmas.map((dma: { code: string; name: string }) => dma.name);

    return { codes, names };
};
