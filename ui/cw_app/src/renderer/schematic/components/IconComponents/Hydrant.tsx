export const Distribution = () => {
    return (
        <svg
            width="40"
            height="60"
            viewBox="0 0 50 80"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <circle cx="25" cy="25" r="21" stroke="white" strokeWidth="2" />
            <circle cx="25" cy="55" r="21" stroke="white" strokeWidth="2" />
            <circle cx="25" cy="25" r="20" fill="#009EDE" />
            <circle cx="25" cy="55" r="20" fill="#009EDE" />
        </svg>
    );
};

export const Double = () => {
    return (
        <svg
            width="40"
            height="55"
            viewBox="0 0 50 75"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <g clip-path="url(#clip0_291_862)">
                <circle
                    cx="25"
                    cy="25"
                    r="21"
                    stroke="white"
                    strokeWidth="2"
                />
                <circle
                    cx="25"
                    cy="55"
                    r="21"
                    stroke="white"
                    strokeWidth="2"
                />
                <circle cx="25" cy="25" r="20" fill="black" />
                <circle cx="25" cy="50" r="20" fill="black" />
            </g>
            <defs>
                <clipPath id="clip0_291_862">
                    <rect width="50" height="75" fill="white" />
                </clipPath>
            </defs>
        </svg>
    );
};

export const Single = () => {
    return (
        <svg
            width="40"
            height="40"
            viewBox="0 0 50 50"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <circle cx="25" cy="25" r="20" fill="black" />
            <circle cx="25" cy="25" r="21" stroke="white" strokeWidth="2" />
        </svg>
    );
};
