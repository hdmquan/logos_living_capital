class Prompt:
    balance_sheet = """ 
        {balance_sheet}
        
        Analyze the balance sheet of this retirement home to assess its financial health and performance. Explain the significance of key financial ratios and trends in the context of the company’s operations. Provide insights into how these trends impact the company’s financial health and performance.
    """

    income_statement = """
        {income_statement}

        Analyze the income statement of this retirement home to assess its financial health and performance. Provide a narrative that connects the income statement to broader financial trends, variances, and company operations. Highlight any notable changes and explain their potential causes and implications.
    """

    revenue = """
        {revenue_detailed}

        Analyze the revenue details of this retirement home to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    labor = """
        {labor}

        Analyze the labor data of this retirement home to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    is_month_comparative = """
        This is the company top 10 percentage variance:
        {percent_var_top}
        
        This is the company top 10 dollar variance:
        {dollar_var_top}

        Analyze the finance variance data of this retirement home to assess its financial health and performance. Explain the underlying reasons for these variances and their implications on the company’s financial health and operations. Provide a clear and concise narrative that links these variances to broader financial performance.
    """

    master = """
        Using the analyses above, compile a comprehensive financial narrative for the retirement home. Explain the story behind the numbers, including causes of variances, trends, and potential risks or opportunities. Provide actionable insights and recommendations based on accurate and verified data. Ensure the narrative is concise and adheres to the client’s preferred paragraph style. Pay extra attention to the Variance Analysis. Output in Markdown format, and try to use at least amount of headers as possible.
    """
