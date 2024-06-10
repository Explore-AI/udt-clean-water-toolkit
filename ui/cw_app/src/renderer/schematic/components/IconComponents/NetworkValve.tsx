export const Default = () => {
    // unknown default
    return (
        <svg
            width="20"
            height="20"
            viewBox="0 0 50 50"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <rect
                x="9"
                y="19"
                width="32"
                height="12"
                stroke="white"
                strokeWidth="2"
            />
            <rect x="10" y="20" width="30" height="10" fill="#FD8FF2" />
        </svg>
    );
};

export const Distribution = () => {
    // distribution network valve, open
    return (
        <svg
            width="20"
            height="20"
            viewBox="0 0 50 50"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <rect
                x="9"
                y="19"
                width="32"
                height="12"
                stroke="white"
                strokeWidth="2"
            />
            <rect x="10" y="20" width="30" height="10" fill="#009EDE" />
        </svg>
    );
};
export const OptSiteDefault = () => {
    // operational site non potable, default
    return (
        <svg
            width="20"
            height="20"
            viewBox="0 0 50 50"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <rect
                x="9"
                y="19"
                width="32"
                height="12"
                stroke="white"
                strokeWidth="2"
            />
            <rect x="10" y="20" width="30" height="10" fill="black" />
        </svg>
    );
};

export const OptSiteClosed = () => {
    // operational site, closed
    return (
        <svg
            width="24"
            height="24"
            viewBox="0 0 54 54"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <rect x="3" y="3" width="48" height="48" rx="24" fill="white" />
            <rect
                x="3"
                y="3"
                width="48"
                height="48"
                rx="24"
                stroke="black"
                strokeWidth="2"
            />
            <circle cx="27" cy="27" r="26" stroke="white" strokeWidth="2" />
            <rect x="12" y="22" width="30" height="10" fill="black" />
        </svg>
    );
};

export const OptSiteClosedInoperable = () => {
    // operational site not potable, inoperable closed
    return (
        <svg
            width="24"
            height="24"
            viewBox="0 0 54 54"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <rect x="3" y="3" width="48" height="48" rx="24" fill="white" />
            <rect
                x="3"
                y="3"
                width="48"
                height="48"
                rx="24"
                stroke="black"
                strokeWidth="2"
            />
            <rect x="12" y="22" width="30" height="10" fill="black" />
            <path
                d="M12.2931 41.5771L40.5773 13.2929"
                stroke="#5A5A5A"
                strokeWidth="2"
                stroke-linecap="round"
            />
            <path
                d="M40.5772 41.5771L12.293 13.2929"
                stroke="#5A5A5A"
                strokeWidth="2"
                stroke-linecap="round"
            />
            <circle cx="27" cy="27" r="26" stroke="white" strokeWidth="2" />
        </svg>
    );
};

export const OptSiteInoperable = () => {
    // operational site not potable, inoperable
    return (
        <svg
            width="20"
            height="20"
            viewBox="0 0 50 50"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <path
                d="M10.2931 39.5773L38.5773 11.293"
                stroke="white"
                strokeWidth="6"
                stroke-linecap="round"
            />
            <path
                d="M38.5772 39.5773L10.293 11.293"
                stroke="white"
                strokeWidth="6"
                stroke-linecap="round"
            />
            <rect
                x="9"
                y="19"
                width="32"
                height="12"
                stroke="white"
                strokeWidth="2"
            />
            <rect x="10" y="20" width="30" height="10" fill="black" />
            <path
                d="M10.2931 39.5771L38.5773 11.2929"
                stroke="#5A5A5A"
                strokeWidth="2"
                stroke-linecap="round"
            />
            <path
                d="M38.5772 39.5771L10.293 11.2929"
                stroke="#5A5A5A"
                strokeWidth="2"
                stroke-linecap="round"
            />
        </svg>
    );
};
